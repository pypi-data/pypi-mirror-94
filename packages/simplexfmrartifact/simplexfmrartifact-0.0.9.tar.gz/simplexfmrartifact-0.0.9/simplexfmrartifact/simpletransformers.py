import json
import os

from bentoml.exceptions import (
    InvalidArgument,
    MissingDependencyException,
)
from bentoml.service import BentoServiceArtifact
import torch

DEFAULT_MODEL_OPTS = {
    'args': {
        'use_multiprocessing': False,
        'silent': True,
    },
    'use_cuda': False,
}


class SimpleTransformersModelArtifact(BentoServiceArtifact):

    def __init__(self, name):
        super(SimpleTransformersModelArtifact, self).__init__(name)
        print('SimpleTransformersModelArtifact name:', name)
        self._model = None
        self._model_opts = None
        self._config = None

    def _file_path(self, base_path):
        return os.path.join(base_path, self.name)

    def _load_config(self, path):
        filepath = os.path.join(path, 'config.json')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                config = json.load(f)
        else:
            config = {}

        self._config = config

    def _load_model_opts(self, path):
        filepath = os.path.join(path, 'model_opts.json')
        print('Loading model opts from', filepath)
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                opts = json.load(f)
        else:
            opts = DEFAULT_MODEL_OPTS

        self._model_opts = opts

    def _load_from_directory(self, path, opts=None, update=False):
        if opts is None:
            self._load_model_opts(path)
        elif update:
            self._load_model_opts(path)
            self._model_opts['opts'].update(opts)
        else:
            self._model_opts = opts

        print('opts:', json.dumps(self._model_opts, indent=4))
        try:
            classname = self._model_opts['classname']
            mod = __import__(self._model_opts['classpackage'], fromlist=[classname])
            clz = getattr(mod, classname)
        except Exception as e:
            print(str(e))
            raise MissingDependencyException(
                'A simpletransformers.classification model is required to use SimpleTransformersModelArtifact'
            )

        self._load_config(path)
        # num_labels isn't consistently defined in config.json
        # kwargs = {
        #     #'num_labels': self._config.get('_num_labels', len(self._config['id2label'])),
        # }
        # kwargs.update(self._model_opts['opts'])
        kwargs = self._model_opts['opts']

        self._model = clz(
            self._config.get('model_type', 'roberta'),
            path,
            **kwargs
        )
    
    def _load_from_dict(self, model, opts=None):
        if not model.get('model'):
            raise InvalidArgument(
                "'model' key is not found in the dictionary. "
                "Expecting a dictionary with keys 'model'"
            )

        if opts is None:
            self._model_opts = model.get('model_opts', DEFAULT_MODEL_OPTS)
        else:
            self._model_opts = opts

        self._model = model

    def pack(self, model, opts=None, update=False):
        if isinstance(model, str):
            if os.path.isdir(model):
                self._load_from_directory(model, opts, update)
            else:
                raise InvalidArgument('Expecting a path to the model directory')
        elif isinstance(model, dict):
            self._load_from_dict(model, opts)
        else:
            raise InvalidArgument('Expecting model to be a path to the model directory or a dict')

        return self

    def load(self, path):
        path = self._file_path(path)
        return self.pack(path)

    def _save_model_opts(self, path, opts):
        with open(os.path.join(path, 'model_opts.json'), 'w') as f:
            json.dump(opts, f)

    def save(self, dst):
        path = self._file_path(dst)
        os.makedirs(path, exist_ok=True)
        self._save_model_opts(path, self._model_opts)
        model = self._model.model
        model_to_save = model.module if hasattr(model, 'module') else model
        model_to_save.save_pretrained(path)
        self._model.tokenizer.save_pretrained(path)
        torch.save(self._model.args, os.path.join(path, 'training_args.bin'))
        return path

    def get(self):
        return self._model
