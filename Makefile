NAME    := Czech Coder
BUNDLE  := $(NAME).bundle
BADGE   ?= CZ

.PHONY: all clean install

all:
	BADGE="$(BADGE)" src/gen_bundle.sh

# Install for the current macOS user (run this ON the Mac).
install: all
	mkdir -p "$(HOME)/Library/Keyboard Layouts"
	rm -rf "$(HOME)/Library/Keyboard Layouts/$(BUNDLE)"
	cp -R "$(BUNDLE)" "$(HOME)/Library/Keyboard Layouts/"
	@echo "Installed. Log out/in, then add 'Czech Coder' in System Settings > Keyboard > Input Sources."

clean:
	rm -rf "$(BUNDLE)"
