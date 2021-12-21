from rest_framework.renderers import JSONRenderer as DrfJSONRenderer


class JSONRenderer(DrfJSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Make all responses with in the same format
        {
            'data': 'This is will be all responses'
        }

        """
        if data is not None:
            if 'results' in data:
                # Handle default paginator response
                data['data'] = data['results']
                del data['results']
            elif isinstance(data, list):
                data = {
                    'data': data
                }
        return super().render(data, accepted_media_type, renderer_context)
