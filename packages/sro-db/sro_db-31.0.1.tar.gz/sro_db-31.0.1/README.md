# Scrum Reference Ontology Lib

## General Information
* **Software**: SRO LIb
* **Author**:Paulo Sérgio dos Santos Júnior
* **Author's e-mail**:paulossjunior@gmail.com
* **Source Repository**: [https://gitlab.com/ontologyasaservice/data/domain/scrum-reference-ontology/sro_db](https://gitlab.com/ontologyasaservice/data/domain/scrum-reference-ontology/sro_db)  

## Goal
This lib is responsible for creating database and operation based on Scrum Reference Ontology.

## Generate documentation

To create the code documentation:
```bash
pdoc --html --force sro_db/ --output docs

```
### Acess code documentation	

To accesss the documenation, go to folder docs/sro_db and open index.html 

To run documentation server: pdoc sro_db --http localhost:8000 

## Instalation
To install sro_db, run this command in your terminal:
	
```bash
pip install sro_db
```

## Usage

## Creating a Database

```python
from sspo_db.config.config import Config
from sspo_db.model.activity.models import *
from sspo_db.service.activity.service import *
from sspo_db.model.core.models import *
from sspo_db.service.core.service import *
from sspo_db.model.stakeholder_participation.models import *

conf = Config()
conf.create_database()
```

## Creating an Organization

```python

from sspo_db.model.organization.models import *
from sspo_db.model.core.models import *
from sspo_db.service.organization.service import *
from sspo_db.service.core.service import *
from pprint import pprint 

#Creating a Organization
organization = Organization()
organization.name = "xxxxxx"
organization.description = "YYYYYY"

organizationService = OrganizationService()
organizationService.create(organization)

```

## Copyright
This lib was PowerRight by [SEON Lib Generator](https://gitlab.com/mdd_seon/ontology-as-a-service/from-ontology-information-model-to-services)
	

