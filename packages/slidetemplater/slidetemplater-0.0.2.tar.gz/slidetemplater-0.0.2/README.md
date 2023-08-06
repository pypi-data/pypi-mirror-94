# SlideTemplater.com Python API

This is a simple client API for SlideTemplater.com

Please see documentation there for how to prepare a presentation for templating

You can use it as the following:

~~~
import slidetemplater.api

result = slidetemplater.api.convert(open(
    'covid.pptx', 'rb'), "https://api.coronavirus.data.gov.uk/v2/data?areaType=overview&metric=cumPeopleVaccinatedFirstDoseByVaccinationDate&format=json")

f = open('result.pptx', 'w+b')
f.write(result)
f.close()
~~~