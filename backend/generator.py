import google.generativeai as genai
from faker import Faker
import pandas as pd
import random
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash')
fake  = Faker('en_IN')

# ── STEP 1: Ask Gemini to understand the prompt ───────
def get_schema(prompt):
    system = '''
You are a dataset schema generator.
Return ONLY a valid JSON object. No explanation. No markdown. Just pure JSON.

Format:
{
  "columns": [
    {"name": "column_name", "type": "name"},
    {"name": "column_name", "type": "integer", "min": 1, "max": 100},
    {"name": "column_name", "type": "float", "min": 0.0, "max": 100.0},
    {"name": "column_name", "type": "date"},
    {"name": "column_name", "type": "email"},
    {"name": "column_name", "type": "phone"},
    {"name": "column_name", "type": "city"},
    {"name": "column_name", "type": "state"},
    {"name": "column_name", "type": "company"},
    {"name": "column_name", "type": "text"},
    {"name": "column_name", "type": "boolean"},
    {"name": "column_name", "type": "uuid"},
    {"name": "column_name", "type": "choice", "values": ["a","b","c"]}
  ]
}

Rules:
- Return ONLY JSON. Nothing else.
- Use realistic min/max values based on the domain
- For choice type always provide meaningful values
- Column names must be lowercase with underscores
- Understand Indian context if mentioned
'''
    response = model.generate_content(system + '\n\nDataset needed: ' + prompt)
    raw      = response.text.strip()
    raw      = re.sub(r'```json|```', '', raw).strip()
    return json.loads(raw)

# ── STEP 2: Generate one value based on column type ───
def generate_value(col):
    t = col.get('type', 'text')
    if   t == 'name':    return fake.name()
    elif t == 'integer': return random.randint(col.get('min',1), col.get('max',100))
    elif t == 'float':   return round(random.uniform(col.get('min',0.0), col.get('max',100.0)), 2)
    elif t == 'date':    return str(fake.date_between(start_date='-2y', end_date='today'))
    elif t == 'email':   return fake.email()
    elif t == 'phone':   return fake.phone_number()
    elif t == 'city':    return fake.city()
    elif t == 'state':   return fake.state()
    elif t == 'country': return fake.country()
    elif t == 'address': return fake.address().replace('\n', ', ')
    elif t == 'company': return fake.company()
    elif t == 'text':    return fake.sentence(nb_words=6)
    elif t == 'boolean': return random.choice([True, False])
    elif t == 'uuid':    return str(fake.uuid4())[:8].upper()
    elif t == 'choice':  return random.choice(col.get('values', ['Option A', 'Option B']))
    else:                return fake.word()

# ── STEP 3: Generate full dataset ─────────────────────
def generate_dataset(prompt, rows):
    schema  = get_schema(prompt)
    columns = schema['columns']
    data    = []
    for _ in range(rows):
        row = {col['name']: generate_value(col) for col in columns}
        data.append(row)
    df = pd.DataFrame(data)
    return df, columns
