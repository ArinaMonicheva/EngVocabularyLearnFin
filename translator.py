#from transformers import T5ForConditionalGeneration, T5Tokenizer
#
#model_name = 'jbochi/madlad400-3b-mt'
#model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")
#tokenizer = T5Tokenizer.from_pretrained(model_name)
#
#text = "<2pt> I love pizza!"
#input_ids = tokenizer(text, return_tensors="pt").input_ids.to(model.device)
#outputs = model.generate(input_ids=input_ids)
#
#tokenizer.decode(outputs[0], skip_special_tokens=True)
## Eu adoro pizza!
#
#
import argostranslate.package
import argostranslate.translate

from_code = "en"
to_code = "ru"

# Download and install Argos Translate package
argostranslate.package.update_package_index()
available_packages = argostranslate.package.get_available_packages()
package_to_install = next(
    filter(
        lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
    )
)
argostranslate.package.install_from_path(package_to_install.download())

# Translate
translatedText = argostranslate.translate.translate("Hello World", from_code, to_code)
print(translatedText)
# '¡Hola Mundo!'