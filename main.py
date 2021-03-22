import json, random, textwrap
import requests
import cv2

def getCatFact(verbose=False) -> str:
	"""
	Gets cat facts and returns a randomly chosen fact as a string.
	"""
	print("Searching for cat quotes...") if verbose else None 
	response = requests.get("https://cat-fact.herokuapp.com/facts")
	cat_facts = json.loads(response.text)
	if verbose:
		print("Found cat quotes:")
		for i in cat_facts:
			print("\t", i["text"])

	quote = random.choice([i["text"] for i in cat_facts])
	print("Chosen quote:", quote)

	return quote

def getCatPicture(verbose=False) -> str:
	"""
	Gets random cat pictures but only keeps them, if they match the following criteria:
	- not a gif
	- width between 600 and 800
	- height between 500 and 900

	Returns the URL as a string.
	"""
	print("Searching for cat pictures...") if verbose else None
	while True:
		response = requests.get("https://api.thecatapi.com/v1/images/search")
		cat_picture = json.loads(response.text.replace("???", "'"))
		print(cat_picture[0], end="\t") if verbose else None
		if not cat_picture[0]["url"].endswith("gif") and 500 < cat_picture[0]["width"] and 400 < cat_picture[0]["height"]:
			print("Thats good!") if verbose else None
			return cat_picture[0]["url"]
		print("Not good :(") if verbose else None

	

def downloadPicture(url:str) -> None:
	"""
	Downloads the picture of Parameter url and saves it locally.
	"""

	url = getCatPicture()
	file_ending = url.split(".")[-1]
	response = requests.get(url, allow_redirects=True)

	with open(f"cat_pic.{file_ending}", "wb") as file:
		file.write(response.content)

	return f"cat_pic.{file_ending}"

def writeOnImage(img_path, verbose=False):

	text = getCatFact(verbose)
	wrapped_text = textwrap.wrap(text, width=35)

	img = cv2.imread(img_path)
	img = cv2.blur(img, (10,10))

	font = cv2.FONT_HERSHEY_SIMPLEX 
	fontScale = 1
	white = (255, 255, 255)
	black = (0, 0, 0)
	thickness = 6

	for i, line in enumerate(wrapped_text):
		textsize = cv2.getTextSize(line, font, fontScale, thickness)[0]
		gap = textsize[1] + 10

		y = int((img.shape[0] + textsize[1]) / 2) + i * gap
		x = int((img.shape[1] - textsize[0]) / 2) 

		img = cv2.putText(img, line, (x, y), font, fontScale, black, thickness, cv2.LINE_AA)
		img = cv2.putText(img, line, (x, y), font, fontScale, white, thickness-4, cv2.LINE_AA)

	cv2.imwrite("nu_cat_pic.jpg", img)

	cv2.imshow("Cat Fact", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows() 


########################################
verbose = True
cat_pic_url = getCatPicture(verbose)
cat_pic_path = downloadPicture(cat_pic_url)
writeOnImage(cat_pic_path, verbose)