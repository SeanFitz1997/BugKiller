from bug_killer_api_interface.interface.api_interface import BUG_KILLER_API


API_DOC_OUTPUT_FILE_NAME = 'api_doc.yml'

if __name__ == '__main__':
    api = BUG_KILLER_API.to_open_api_doc()
    with open(API_DOC_OUTPUT_FILE_NAME, 'w') as f:
        f.write(api.to_yaml())
