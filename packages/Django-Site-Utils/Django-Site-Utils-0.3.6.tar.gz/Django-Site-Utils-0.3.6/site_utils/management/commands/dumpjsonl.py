# Python
import bz2
import collections
import gzip
import json
import logging
import sys

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.core import serializers

# Django Extensions
from django_extensions.management.modelviz import ModelGraph


class Command(BaseCommand):

    help = 'Output the contents of the database as JSONL.'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('-o', '--output', default='-', help='Output file '
                            'for JSONL output (default is stdout).',
                            metavar='OUTPUT')
        parser.add_argument('--compression', default='auto', choices=['auto',
                            'gzip', 'bzip2', 'none'], help='Type of '
                            'compression to apply to JSONL output (auto will '
                            'select gzip if output filename ends with `.gz`, '
                            'bzip2 if filename ends with `.bz2`, or none '
                            'otherwise.', metavar='COMPRESSION')

    def init_logging(self):
        log_levels = dict(enumerate([logging.ERROR, logging.INFO,
                                     logging.DEBUG, 0]))
        logging.getLogger('iso8601').setLevel(logging.WARNING)
        logging.getLogger('django.db.backends').setLevel(log_levels.get(self.verbosity, 0) + 10)
        self.logger = logging.getLogger()
        self.logger.setLevel(log_levels.get(self.verbosity, 0))
        handler = logging.StreamHandler(self.stderr)
        handler.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
        handler.terminator = ''
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def model_class_display(self, model_class):
        return '{}.{}'.format(model_class._meta.app_label, model_class._meta.model_name)

    def get_initial_model_dependencies(self):
        graph_models = ModelGraph([], all_applications=True)
        graph_models.generate_graph_data()
        graph_data = graph_models.get_graph_data(as_json=True)
        model_classes = {}
        model_depmap = collections.OrderedDict()

        for app_data in graph_data['graphs']:
            app_name = app_data['app_name']
            app_config = apps.get_app_config(app_name.split('.')[-1])
            app_abstract_models = graph_models.get_abstract_models(app_config.get_models())
            for model_data in app_data['models']:
                model_app_name = model_data['app_name']
                model_name = model_data['name']
                try:
                    model_class = app_config.get_model(model_name)
                except LookupError:
                    model_class = [m for m in app_abstract_models if m.__name__ == model_name][0]
                self.logger.debug('graph model: %s.%s -> %s', model_app_name, model_name, self.model_class_display(model_class))
                model_classes[(model_app_name, model_name)] = model_class
                model_depmap[(model_app_name, model_name)] = []
                for relation_data in model_data['relations']:
                    target_app_name = relation_data['target_app']
                    target_model_name = relation_data['target']
                    target_type = relation_data['type']
                    self.logger.debug('- graph dep: %s.%s (%s)', target_app_name, target_model_name, target_type)
                    model_depmap[(model_app_name, model_name)].append((target_app_name, target_model_name))

        model_depends = collections.OrderedDict()
        for model_lookup, target_lookups in model_depmap.items():
            model_class = model_classes[model_lookup]
            target_classes = []
            for target_lookup in target_lookups:
                target_class = model_classes.get(target_lookup)
                if target_class and target_class not in target_classes:
                    target_classes.append(target_class)
            model_depends[model_class] = target_classes

        return model_depends

    def sort_model_dependencies(self, model_depends, iterations=10):
        order_changed = False
        for iteration in range(1, iterations + 1):
            self.logger.debug('sorting model dependencies, iteration %d', iteration)
            order_changed = False
            model_depends_new = collections.OrderedDict()
            for model_class, target_classes in model_depends.items():
                if target_classes:
                    targets_display = ', '.join(map(self.model_class_display, target_classes))
                else:
                    targets_display = 'nothing'
                self.logger.debug('- %s depends on %s', self.model_class_display(model_class), targets_display)
                for target_class in target_classes:
                    if target_class not in model_depends_new:
                        model_depends_new[target_class] = model_depends[target_class]
                        order_changed = True
                if model_class not in model_depends_new:
                    model_depends_new[model_class] = target_classes
            model_depends = model_depends_new
            if not order_changed:
                break
        if order_changed:
            self.logger.error('unable to sort model dependencies after %d iterations', iterations)
            raise RuntimeError()
        else:
            self.logger.debug('finished sorting model dependencies')
            return model_depends

    def get_sorted_model_classes(self, model_depends):
        model_classes = []
        from django.db.migrations.recorder import MigrationRecorder
        model_classes.append(MigrationRecorder.Migration)
        for model_class in model_depends.keys():
            if model_class._meta.abstract or model_class._meta.proxy:
                continue
            model_classes.append(model_class)
        return model_classes

    def open_output_file(self, filename='-', compression='auto'):
        if not filename or filename == '-':
            self.logger.info('writing output to stdout')
            return sys.stdout
        elif filename.endswith('.gz') and compression == 'auto' or compression == 'gzip':
            self.logger.info('writing gzip output to %s', filename)
            return gzip.GzipFile(filename, 'wb')
        elif filename.endswith('.bz2') and compression == 'auto' or compression == 'bzip2':
            self.logger.info('writing bzip2 output to %s', filename)
            return bz2.BZ2File(filename, 'w')
        else:
            self.logger.info('writing output to %s', filename)
            return open(filename, 'wb')

    def dump_to_jsonl(self, model_class, output_file):
        self.logger.info('%d instances of %s', model_class.objects.count(),
                         self.model_class_display(model_class))
        qs = model_class.objects.order_by('pk')
        if model_class._meta.model_name == 'hubspotcallback':
            qs = qs.defer('request_data')
        n = 0
        for n, instance in enumerate(qs.iterator()):
            json_data = serializers.serialize('json', [instance])
            instance_data = json.loads(json_data)[0]
            if n == 0:
                self.logger.debug('model: %s', instance_data['model'])
            json_data = json.dumps(instance_data).replace('\n', ' ').strip()
            output_file.write(('%s\n' % json_data).encode('utf8'))
            if n % 500 == 0 and self.verbosity >= 1:
                self.stderr.write('.', ending='')
                self.stderr.flush()
        if n > 0 and self.verbosity >= 1:
            self.stderr.write('')
            self.stderr.flush()

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity', 1))
        self.output = options.get('output', '-')
        self.compression = options.get('compression', 'auto')
        self.init_logging()
        model_depends = self.get_initial_model_dependencies()
        model_depends = self.sort_model_dependencies(model_depends)
        model_classes = self.get_sorted_model_classes(model_depends)
        with self.open_output_file(self.output, self.compression) as output_file:
            for model_class in model_classes:
                self.dump_to_jsonl(model_class, output_file)
