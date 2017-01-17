(setq make-backup-files nil)
(add-to-list 'default-frame-alist '(font . "Cousine-8"))

(setq-default c-basic-offset 4)
(setq-default indent-tabs-mode nil)

(menu-bar-mode -1)
(scroll-bar-mode -1)
(tool-bar-mode -1)
(column-number-mode 1)

(global-linum-mode 1)

(require 'uniquify)

(setq evil-default-cursor t
      evil-want-C-i-jump t
      evil-want-C-u-scroll t)
(require 'evil)
(evil-mode 1)

(autoload 'rust-mode "rust-mode" nil t)
(add-to-list 'auto-mode-alist '("\\.rs\\'" . rust-mode))

(setq font-latex-fontify-sectioning 'color)
(setq font-latex-script-display (quote (nil)))

(custom-set-faces
 '(font-latex-subscript-face ((t nil)))
 '(font-latex-superscript-face ((t nil))))

(setq font-latex-deactivated-keyword-classes
 '("italic-command" "bold-command" "italic-declaration" "bold-declaration"))

(add-to-list 'custom-theme-load-path "/usr/share/emacs/etc/themes/")
(load-theme 'solarized t)
