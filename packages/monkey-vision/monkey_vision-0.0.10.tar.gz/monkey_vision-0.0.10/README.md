# monkey-vision - `UNSTABLE`

```bash
##################################
###        monkey vision       ###
##################################
```

Computer vision image analyses for monkey screenshots.
This module can analyze app screenshots and provide information about all the intractable components in the image.

# Install

Install the package. If you prefer you can use a virtual environment. **(Check [docs/README.md](/docs/README.md))**

```bash
 $ pip install monkey_vision
```

To get a specific version or to check for updates please refer to the [Links](#Links) section.

# Exposed api

1. Image analysis, get image event point.
Will return the list of possible interaction coordinates (event points) visible in the provided screenshot. 

```bash
 $ monkey_vision -r imagePath
 $ monkey_vision --run imagePath
```

2. Percentage compare between two images:
Will return the calculated percentage of the match between two provided images.

```bash
 $ monkey_vision -m imagePath1 imagePath2
 $ monkey_vision --match imagePath1 imagePath2
```

3. Help:
```bash

 $ monkey_vision -h
 $ monkey_vision --help
```


# Links 

- Production releases are published at [PyPI](https://pypi.org/project/monkey-vision/).
- For test or/and unstable versions check out [TestPyPI](https://test.pypi.org/project/monkey-vision/).

