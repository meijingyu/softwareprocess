import Fix 
theFix = Fix.Fix()
sightingFilePath = theFix.setSightingFile("sightings.xml")
starFilePath = theFix.setStarFile("star.txt")
ariesFilePath = theFix.setAriesFile("aries.txt")
assumedLatitude = "-53d38.4"
assumedLongitude = "74d35.3"
approximatePosition = theFix.getSightings(assumedLatitude, assumedLongitude)