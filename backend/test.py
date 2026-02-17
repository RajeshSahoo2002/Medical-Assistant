import google.genai as genai # type: ignore

for m in genai.list_models():
    print(m.name, m.supported_generation_methods)