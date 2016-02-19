import sys
import argparse
from bs4 import BeautifulSoup
import urllib2

def main():
    url = "http://dogtime.com/dog-breeds/"
    dogs = ["chow-chow", "dalmatian", "dachshund", "golden-retriever", 
            "mastiff", "pocket-beagle", "rottweiler", "irish-terrier", 
            "boxer", "chinese-shar-pei", "bichon-frise", "dogue-de-bordeaux"]
    wantedCharacteristics = ["Tolerates Being Alone",
                             "Tolerates Cold Weather",
                             "Kid Friendly",
                             "Amount Of Shedding",
                             "Drooling Potential",
                             "Easy To Groom",
                             "Size",
                             "Intelligence",
                             "Energy Level",
                             "Exercise Needs"
                            ]
    prologCharacteristics = ["AloneCapabilitiesLevel", 
			     "ColdWeatherTolerance", 
			     "KidFriendly", 
			     "SheddingLevel", 
			     "DroolingLevel", 
			     "GroomLevel", 
			     "Size", 
			     "IntelligenceLevel", 
			     "EnergyLevel", 
			     "ExerciseRequirementLevel"
                            ]
    savedDogs = []

    for dog in dogs:
        dogName = dog.replace('-', ' ').title().replace(' ', '_')
        response = urllib2.urlopen(url + dog)
        source = response.read()

        soup = BeautifulSoup(source, "lxml")
        characteristics = soup.findAll('a', {'class': 'js-list-item-trigger item-trigger more-info'})

        curDog = {}
        curDog['name'] = dogName

        for characteristic in characteristics:
            title = characteristic.find('span', {'class' : "characteristic item-trigger-title"})
            stars = characteristic.find('span', {'class' : "star"})
            titleText = title.text.strip()
            starText = stars.text.strip()
            if titleText in wantedCharacteristics:
                curDog[prologCharacteristics[wantedCharacteristics.index(titleText)]] = int(starText)

        savedDogs.append(curDog)

    for dog in savedDogs:
        print """
        <!-- http://www.example.com/dog.owl#{} -->

        <owl:NamedIndividual rdf:about="http://www.example.com/dog.owl#{}">
            <rdf:type rdf:resource="http://www.example.com/dog.owl#Dog"/>
            <AloneCapabilitiesLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</AloneCapabilitiesLevel>
            <ColdWeatherTolerance rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</ColdWeatherTolerance>
            <DroolingLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</DroolingLevel>
            <EnergyLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</EnergyLevel>
            <ExerciseRequirementLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</ExerciseRequirementLevel>
            <GroomLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</GroomLevel>
            <IntelligenceLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</IntelligenceLevel>
            <KidFriendly rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</KidFriendly>
            <SheddingLevel rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</SheddingLevel>
            <Size rdf:datatype="http://www.w3.org/2001/XMLSchema#integer">{}</Size>
        </owl:NamedIndividual>
        """.format(dog.get('name'), dog.get('name'), dog.get('AloneCapabilitiesLevel'), dog.get('ColdWeatherTolerance'),
                   dog.get('DroolingLevel'), dog.get('EnergyLevel'), dog.get('ExerciseRequirementLevel'), dog.get('GroomLevel'),
                   dog.get('IntelligenceLevel'), dog.get('KidFriendly'), dog.get('SheddingLevel'), dog.get('Size'))
    return 0

if __name__ == "__main__":
    sys.exit(main())
