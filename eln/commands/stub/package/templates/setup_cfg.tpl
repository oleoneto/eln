[metadata]
name = {{ package }}
description =
license_file = LICENSE.txt
long-description = file: README.md
platforms = any

[bdist_wheel]
universal = 1

[tool:pytest]
testpaths = tests

[coverage:run]
branch = True
source =
    {{ package }}
    tests

[coverage:paths]
source =
    {{ package }}
