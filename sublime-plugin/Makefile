.PHONY: install uninstall

PLUGIN = ~/.config/sublime-text-3/Packages/Vasilek
SUBLIME = ~/.config/sublime-text-3

install:
	@if [ ! -d $(SUBLIME) ]; then \
		echo "Can't find sublime config"; \
	else \
		cp -r Vasilek/ $(PLUGIN); \
	fi 

uninstall:
	@if [ ! -d $(SUBLIME) ]; then \
		echo "Can't find sublime config"; \
	else \
		rm -rd $(PLUGIN); \
	fi