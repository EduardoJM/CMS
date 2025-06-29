import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler,
)


class CodeBlockElementHandler(BlockElementHandler):
    def create_block(self, name, attrs, state, contentstate):
        # print(state)
        # print(dir(state))
        return super().create_block(name, attrs, state, contentstate)

@hooks.register('register_rich_text_features')
def register_code_block_feature(features):
    feature_name = 'custom-code'
    type_ = 'custom-code'
    tag = 'pre'

    control = {
        'type': type_,
        'label': '{}',
        'description': 'Code',
    }

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.BlockFeature(control)
    )

    features.register_converter_rule('contentstate', feature_name, {
        'from_database_format': {
            tag: CodeBlockElementHandler(type_),
        },
        'to_database_format': {
            'block_map': {
                type_: tag
            }
        },
    })

    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_prism(features):
    feature_name = 'prism'
    features.default_features.append(feature_name)

    features.register_editor_plugin(
        'draftail',
        feature_name,
        draftail_features.PluginFeature(
            {
                'type': feature_name,
            },
            css={ 'all': ['draftail/vendor/prism.min.css'] },
            js=[
                'draftail/vendor/prism.min.js',
                'draftail/vendor/immutable.min.js',
                'draftail/draftail-prism.js',
            ],
        ),
    )
