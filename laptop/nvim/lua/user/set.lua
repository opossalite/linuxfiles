vim.opt.nu = true
vim.opt.relativenumber = true

vim.opt.tabstop = 4
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true

vim.opt.smartindent = true
vim.opt.wrap = false

vim.opt.swapfile = false
vim.opt.backup = false
vim.opt.undodir = os.getenv("HOME") .. "/.vim/undodir"
vim.opt.undofile = true

vim.opt.hlsearch = false
vim.opt.incsearch = true

vim.opt.termguicolors = true

vim.opt.scrolloff = 8
vim.g.mapleader = " "

vim.cmd("autocmd FileType * set formatoptions-=cro")

--vim.g.NERDTreeHijackNetrw = 0
--vim.g.lf_replace_netrw = 1
vim.g.lf_width = 1920
vim.g.lf_height = 1080

