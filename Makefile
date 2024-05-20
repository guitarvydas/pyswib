all:
	@echo 'ensure that formatted text option in draw.io is disabled everywhere'
	./0d/das2json/das2json pyswib.drawio
	python3 main.py . 0D/python test.txt main pyswib.drawio.json
