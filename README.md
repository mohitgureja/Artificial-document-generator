# Artificial Document Generator

The artificial document generator generate realistic document images for any document category using user-defined
configurations. The software generates context-relevant data utilizing a Generative Pre-trained Transformer (GPT) model
and renders this generated data on the canvas using randomization in user-defined style preferences.

This page gives step-by-step instructions to install and use the software. The effectiveness of its approach has also
been demonstrated through the configuration files provided for invoices and resume dataset.

## Prerequisites

The current version of the generator relies on Python 3.8+ and uses OpenAI GPT 3.5-turbo along with certain requirements
mentioned in requirements.txt file.

- Python 3.8+: Currently tested with Python 3.9 and 3.11
- OpenAI: Currently tested with GPT 3.5-turbo (others can also be configured)

## Installation

To install requirements, run the following command from the root directory of the project:

- `pip install -r requirements.txt`

## Using generator

The current software operates as a backend API developed with FastAPI in Python. You can run this command from the root
directory to initiate the API:

- `python index.py` <br>
  API starts in localhost at http://127.0.0.1:8000

It comprises two API endpoints.

1. The first is a GET request with `/config` endpoint to retrieve category specific parameters needed to generate
   document dataset for that particular category.
   For example, the <i>invoice</i> specific parameters can be retrieved using following curl request:
   ````
    curl --location 'http://127.0.0.1:8000/config?doc_format=invoice'
    ```` 
   Response:
   ````
    invoice_params: { "address": true, "rechnungsnummer": true, "product_name": true,
        "product_amount": true, "customer_name": true, "organization": true, "amount_sentence": true, 
        "bank_iban": true, "bank_swift": true, "organization_address": true, "organization_contact": true,
        "date": true, "diagnose": true }
   ````
   Similarly, using `doc_format=resume` returns the parameters for generating resume. This request shall only work if
   the parameters configuration file [request.json](data/request/request.json) is already present at '<i>
   data/request/request.json</i>'. <br><br>

2. The second is the primary API endpoint for initiating the document generation workflow. It operates as a POST request
   and can be accessed at `/create` endpoint. In the request body, it is necessary to specify configuration and
   category-specific parameters. If you need to generate data using GPT, then please provide the OpenAI key in the
   environment using `OPENAI_API_KEY=""`. Below is an illustration of a CURL request for generating invoices.
    ````
   curl --location 'http://127.0.0.1:8000/create?doc_format=invoice' \
    --header 'Content-Type: application/json' \
    --data {
        "count": 10,
        "augmentation":false,
        "data_rendering": true,
        "groundtruth_format": "json",
        "gpt_enabled": true,
        "countries": ["de_DE"],
        invoice_params: { "address": true, "rechnungsnummer": true, "product_name": true,
            "product_amount": true, "customer_name": true, "organization": true, "amount_sentence": true, 
            "bank_iban": true, "bank_swift": true, "organization_address": true, "organization_contact": true,
            "date": true, "diagnose": true }
    }
    ````

   It starts the documents generation process. The response gives the location of the generated images from the root
   folder.

   Response:
      ````
    {
      "Generated data": "data/invoice/input/renderer/invoice.json",
      "Generated images": "data/invoice/output/images/",
      "Ground truth data": "data/invoice/output/groundtruth/"
   }
      ````
   If Data Augmentation is turned on in the request, then response also returns the location of augmented images.

## Configuration

Currently, four JSON files are required to configure data generation and rendering using style templates. Following
table presents the configuration files for invoice documents and their respective functionality.

| Configuration file                                                       | Component      | Function                                     |
|--------------------------------------------------------------------------|----------------|----------------------------------------------|
| [config.json](data/invoice/input/generator/config.json)                  | Data Generator | GPT and Faker configurations                 |
| [page_config.json](data/invoice/input/renderer/page_config.json)         | Data Renderer  | Page design configurations                   |
| [position_config.json](data/invoice/input/renderer/position_config.json) | Data Renderer  | Block and data fields related configurations |
| [style_config.json](data/invoice/input/renderer/style_config.json)       | Data Renderer  | Style/Markdown specific configurations       |

Note: There is a need to prepare style templates for each of the configuration file in Data Renderer component. 