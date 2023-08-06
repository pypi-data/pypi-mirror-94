# Pelican Markdown Image Processor
This pelican plugin allows you to use native markdown syntax to reference images,
no matter whether the image is in your statics folder. This can help you use whatever
directory structure to store the images.

## Installation
`pip install pelican-markdown-image`

## Development
Generating distribution archives:
`python -m build`

Install this package in development mode:
`pip install -e . --no-build-isolation`
(We must add the --no-build-isolation option,
this can be a pip's bug)

Upload to pypi:
`twine upload dist/*`
