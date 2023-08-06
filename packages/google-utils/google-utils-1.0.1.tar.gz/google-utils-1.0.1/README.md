# google-utils

Use google from the convenience of a python script!

## Installation

Install from pip:

```bash
pip install google-utils
```

## Usage

Fetching links:

```py
from google_utils import Google

results = Google.search("Minecraft")
for result in results:
    print(result.link)
```

Calculator:

```py
from google_utils import Google

response = Google.calculate("64 to the power of six")
print(f"{response.question}\n{response.answer}")
```

Weather checking:

```py
from google_utils import Google

response = Google.weather("san francisco in celcius")
print(f"{response.weather} {response.temperature}")
```

Definition:

```py
from google_utils import Google

response = Google.define("splendid")
print(f"{response.phrase}, {response.type}\n{response.pronunciation}\n{response.meaning}")
```
