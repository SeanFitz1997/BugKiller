# Commands

Set up pipenv environment __(needed for everything)__

```pipenv shell```

Install dependencies

```pipenv install --dev```

Run tests

```python -m pytest```

Run tests with coverage

```
coverage run --source=bug_killer -m pytest
coverage html
```

Generate requirements file (needed for deployment)

```pipenv lock -r > requirements.txt```

