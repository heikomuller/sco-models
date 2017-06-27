# Model Outputs

For each model a list of possible outputs is specified. Outputs are individual files that the model creates in the output directory. For each file the following information is specified:

- filename
- mimetype

In addition, the filename of the prediction file needs to be specified. This file is always present and therefore listed separate to the attachments. Each attachment is considered optional. If no file with the specified name is present there will be no error.

- outputs:
    - prediction: '... filename ...'
    - attachments:
        - filename: '... filename ...'
        - mimeType: '...'

Attachments are uniquely identified by their name which will also be used to map them to widgets.
