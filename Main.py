from DocumentModel.Document import Document
from StudentModel.StudentModel import StudentModel
import warnings
warnings.simplefilter("ignore")

def runStudent(config, story, vocab, storyName, studentType):
    student = StudentModel(vocab, config)

    document = Document(story, student)

    print(studentType)
    print(storyName)
    predictAndPrint(document)

def predictAndPrint(doc):
    doc.predictDocument()
    doc.organaizeVocab()

    print("Unknown Vocab: ", len(doc.unknownWords.keys()))
    print("Unknown Vocab: ", doc.unknownWords.keys(), "\n")
    print("Easy Vocab: ", len(doc.easyWords.keys()))
    print("Easy Vocab: ", doc.easyWords.keys(), "\n")
    print("Difficult Vocab:", len(doc.difficultWords.keys()))
    print("Difficult Vocab:", doc.difficultWords.keys(), "\n\n")

def loadStudentVocab(path):
    with open(path, "r") as file:
        words = [line.replace("\n", "") for line in file]
    return words

if __name__ == "__main__":
    setBeg = eval("['tired', 'peep', 'sleepy', 'stupid', 'afterwards', 'ought', 'waistcoat', 'hurry', 'curiosity', 'hedge', 'tunnel', 'dip', 'plenty', 'cupboard', 'shelf', 'peg', 'jar', 'disappointment', 'underneath', 'tumble', 'stair', 'brave', 'Would', 'aloud', 'schoolroom', 'presently', 'downwards', 'curtsey', 'fancy', 'curtseying', 'ignorant', 'saucer', 'dreamy', 'doze', 'earnestly', 'bump', 'heap', 'shaving', 'hurt', 'overhead', 'whisker', 'instantly', 'sadly', 'legged', 'curtain', 'keyhole', 'wander', 'fountain', 'doorway', 'shoulder', 'shut', 'telescope', 'lately', 'impossible', 'beautifully', 'wise', 'mark', 'poison', 'beast', 'unpleasant', 'bleed', 'disagree', 'sooner', 'flavour', 'cherry', 'tart', 'custard', 'pine', 'roast', 'toffee', 'butter', 'toast', 'curious', 'feeling', 'brighten', 'shrink', 'altogether', 'possibly', 'plainly', 'slippery', 'tire', 'crying', 'sharply', 'scold', 'unkind', 'croquet', 'pretend', 'hardly', 'respectable', 'ebony', 'creep', 'anxiously', 'surprised', 'dull', 'curiouser', 'stocking', 'bother', 'nonsense', 'hopeless', 'ashamed', 'shed', 'pattering', 'splendidly', 'glove', 'nosegay', 'timid', 'violently', 'skurrie', 'delicious', 'smell', 'queer', 'today', 'yesterday', 'ringlet', 'besides', 'signify', 'doth', 'hoarse', 'crocodile', 'shine', 'tail', 'cheerfully', 'grin', 'neatly', 'claws', 'gently', 'jaw', 'poky', 'burst', 'rapidly', 'hastily', 'splash', 'chin', 'weep', 'swim', 'punish', 'drown', 'walrus', 'hippopotamus', 'inquisitively', 'wink', 'daresay', 'notion', 'quiver', 'fright', 'pardon', 'forgot', 'shrill', 'passionate', 'soothing', 'quiet', 'lazily', 'purr', 'nicely', 'lick', 'paw', 'wash', 'bristle', 'offend', 'positively', 'tremble', 'rage', 'nasty', 'vulgar', 'eagerly', 'eyed', 'terrier', 'curly', 'brown', 'fetch', 'commotion', 'softly', 'passion', 'trembling', 'shore', 'creature']")
    setInt = eval("['peep', 'sleepy', 'stupid', 'daisy', 'remarkable', 'afterwards', 'waistcoat', 'tunnel', 'dip', 'slowly', 'cupboard', 'peg', 'jar', 'underneath', 'tumble', 'brave', 'aloud', 'schoolroom', 'presently', 'downwards', 'curtsey', 'curtseying', 'ignorant', 'saucer', 'bat', 'dreamy', 'earnestly', 'bump', 'heap', 'shaving', 'hurt', 'overhead', 'passage', 'whisker', 'instantly', 'sadly', 'tiny', 'curtain', 'lovely', 'fountain', 'shoulder', 'shut', 'telescope', 'beautifully', 'wise', 'mark', 'poison', 'unpleasant', 'flavour', 'tart', 'custard', 'pine', 'roast', 'toffee', 'butter', 'toast', 'curious', 'brighten', 'shrink', 'possibly', 'plainly', 'slippery', 'tire', 'crying', 'scold', 'unkind', 'croquet', 'hardly', 'respectable', 'ebony', 'creep', 'anxiously', 'dull', 'curiouser', 'stocking', 'nonsense', 'hopeless', 'shed', 'splendidly', 'nosegay', 'desperate', 'timid', 'violently', 'skurrie', 'darkness', 'delicious', 'smell', 'queer', 'today', 'yesterday', 'ringlet', 'besides', 'signify', 'doth', 'strange', 'crocodile', 'shine', 'tail', 'cheerfully', 'grin', 'neatly', 'claws', 'gently', 'jaw', 'poky', 'sudden', 'rapidly', 'hastily', 'chin', 'weep', 'swim', 'walrus', 'hippopotamus', 'inquisitively', 'quiver', 'fright', 'pardon', 'forgot', 'shrill', 'passionate', 'soothing', 'angry', 'quiet', 'lazily', 'purr', 'nicely', 'lick', 'paw', 'wash', 'bristle', 'positively', 'tremble', 'rage', 'nasty', 'vulgar', 'eagerly', 'terrier', 'curly', 'brown', 'fetch', 'softly', 'pale', 'passion', 'trembling', 'shore', 'creature']")
    setAdv = eval("['peep', 'waistcoat', 'cupboard', 'peg', 'brave', 'Would', 'schoolroom', 'presently', 'downwards', 'curtsey', 'curtseying', 'saucer', 'dreamy', 'doze', 'earnestly', 'bump', 'shaving', 'whisker', 'sadly', 'curtain', 'keyhole', 'telescope', 'beautifully', 'mark', 'poison', 'unpleasant', 'bleed', 'flavour', 'tart', 'custard', 'toffee', 'butter', 'toast', 'curious', 'possibly', 'slippery', 'tire', 'scold', 'unkind', 'croquet', 'respectable', 'ebony', 'anxiously', 'curiouser', 'stocking', 'nonsense', 'shed', 'pattering', 'splendidly', 'nosegay', 'timid', 'violently', 'skurrie', 'delicious', 'smell', 'queer', 'yesterday', 'ringlet', 'besides', 'signify', 'doth', 'crocodile', 'shine', 'tail', 'cheerfully', 'grin', 'neatly', 'gently', 'jaw', 'poky', 'rapidly', 'splash', 'weep', 'swim', 'walrus', 'hippopotamus', 'inquisitively', 'daresay', 'quiver', 'fright', 'pardon', 'passionate', 'quiet', 'lazily', 'purr', 'nicely', 'paw', 'bristle', 'positively', 'tremble', 'nasty', 'vulgar', 'eagerly', 'terrier', 'fetch', 'softly', 'trembling', 'shore', 'creature']")

    setBeg = set(setBeg)
    setInt = set(setInt)
    setAdv = set(setAdv)

    overlapBegInt = len(setBeg.intersection(setInt)) / min(len(setBeg), len(setInt))
    overlapIntAddv = len(setAdv.intersection(setInt)) / min(len(setAdv), len(setInt))
    print(overlapBegInt)
    print(overlapIntAddv)
    print("\n\n")

    setBeg = eval("['bachelor', 'intern', 'streaming', 'evaporated', 'coronavirus', 'hostess', 'brew', 'internship', 'foreseeable', 'spokesman', 'temporarily', 'pause', 'intake', 'ceremony', 'unemployment', 'shutter', 'bother', 'counsel', 'coursework', 'rumor', 'bump', 'rescind', 'anxiety', 'mint', 'recruiting', 'worry', 'spokespeople', 'adjustment', 'jeopardy', 'adviser', 'disruption', 'pursue', 'recession', 'grad', 'downturn', 'economist', 'alike', 'pandemic', 'prospect', 'biotech', 'poise', 'workforce', 'hospitality', 'steep', 'majoring', 'recruit', 'frustrating', 'forecaster', 'unprecedented', 'upended', 'disposable', 'digital', 'forensic', 'cybersecurity', 'recruiter', 'expire', 'tout', 'selling']")
    setInt = eval("['journalism', 'intern', 'streaming', 'evaporated', 'coronavirus', 'hostess', 'brew', 'temporarily', 'pause', 'intake', 'ceremony', 'shutter', 'counsel', 'coursework', 'rumor', 'bump', 'rescind', 'anxiety', 'mint', 'spokespeople', 'adjustment', 'jeopardy', 'adviser', 'disruption', 'grad', 'downturn', 'alike', 'pandemic', 'prospect', 'biotech', 'hospitality', 'steep', 'majoring', 'recruit', 'frustrating', 'forecaster', 'unprecedented', 'upended', 'disposable', 'digital', 'forensic', 'cybersecurity', 'recruiter', 'expire', 'tout']")
    setAdv = eval("['streaming', 'evaporated', 'coronavirus', 'hostess', 'foreseeable', 'spokesman', 'temporarily', 'pause', 'intake', 'shutter', 'counsel', 'coursework', 'bump', 'rescind', 'mint', 'spokespeople', 'jeopardy', 'disruption', 'grad', 'downturn', 'economist', 'alike', 'pandemic', 'prospect', 'biotech', 'hospitality', 'steep', 'majoring', 'recruit', 'frustrating', 'forecaster', 'unprecedented', 'upended', 'disposable', 'forensic', 'cybersecurity', 'recruiter', 'expire', 'tout']")

    setBeg = set(setBeg)
    setInt = set(setInt)
    setAdv = set(setAdv)

    overlapBegInt = len(setBeg.intersection(setInt)) / min(len(setBeg), len(setInt))
    overlapIntAddv = len(setAdv.intersection(setInt)) / min(len(setAdv), len(setInt))
    print(overlapBegInt)
    print(overlapIntAddv)


    # advVocabPath = "E:/User/Documents/PycharmProjects/VocabularySetGeneratorPipeline/TestData/TestStudentData/student4.txt"
    # intVocabPath = "E:/User/Documents/PycharmProjects/VocabularySetGeneratorPipeline/TestData/TestStudentData/student2.txt"
    # begVocabPath = "E:/User/Documents/PycharmProjects/VocabularySetGeneratorPipeline/TestData/TestStudentData/student0.txt"
    #
    # alicePath = "E:/User/Documents/PycharmProjects/VocabularySetGeneratorPipeline/TestData/TestStoryData/AliceInWonderland.txt"
    # wsjPath = "E:/User/Documents/PycharmProjects/VocabularySetGeneratorPipeline/TestData/TestStoryData/WSJNews.txt"
    #
    # advancedConfig = {
    #     "bertModel": "bert-large-uncased",
    #     "numberOfGuesses": 60,
    #     "useSynonyms": True,
    #     "useSimilarity": False,
    # }
    #
    # intermediateConfig = {
    #     "bertModel": "bert-large-cased-whole-word-masking",
    #     "numberOfGuesses": 10,
    #     "useSynonyms": False,
    #     "useSimilarity": False,
    # }
    #
    # beginnerConfig = {
    #     "bertModel": "bert-base-multilingual-uncased",
    #     "numberOfGuesses": 50,
    #     "useSynonyms": True,
    #     "useSimilarity": False,
    # }
    #
    # with open(alicePath, "r", encoding='utf8') as file:
    #     aliceStory = file.read()
    #
    # with open(wsjPath, "r", encoding='utf8') as file:
    #     wsjStory = file.read()
    #
    # runStudent(beginnerConfig, aliceStory, loadStudentVocab(begVocabPath), "Alice", "Beginning")
    # runStudent(beginnerConfig, aliceStory, loadStudentVocab(intVocabPath), "Alice", "Beginning2")
    # runStudent(intermediateConfig, aliceStory, loadStudentVocab(intVocabPath), "Alice", "Intermediate")
    # runStudent(advancedConfig, aliceStory, loadStudentVocab(advVocabPath), "Alice", "Advanced")
    # runStudent(advancedConfig, aliceStory, loadStudentVocab(intVocabPath), "Alice", "Advanced2")
    #
    # runStudent(beginnerConfig, wsjStory, loadStudentVocab(begVocabPath), "WSJ", "Beginning")
    # runStudent(beginnerConfig, wsjStory, loadStudentVocab(intVocabPath), "WSJ", "Beginning2")
    # runStudent(intermediateConfig, wsjStory, loadStudentVocab(intVocabPath), "WSJ", "Intermediate")
    # runStudent(advancedConfig, wsjStory, loadStudentVocab(advVocabPath), "WSJ", "Advanced")
    # runStudent(advancedConfig, wsjStory, loadStudentVocab(intVocabPath), "WSJ", "Advanced2")