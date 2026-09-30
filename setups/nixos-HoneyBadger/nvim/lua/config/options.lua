local opt = vim.opt

-- Leader keys (set before plugins load)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- UI
opt.number = true
opt.relativenumber = true
opt.termguicolors = true
opt.signcolumn = "yes" -- reserve space for diagnostic/git signs so text doesn't jump
opt.cursorline = true
opt.scrolloff = 8
opt.splitright = true
opt.splitbelow = true

-- Proper tabbing / indentation
opt.expandtab = true -- spaces, not literal tabs
opt.shiftwidth = 4 -- indent width for autoindent/</></>
opt.tabstop = 4 -- width a literal tab renders as
opt.softtabstop = 4
opt.smartindent = true
opt.autoindent = true
opt.breakindent = true -- wrapped lines keep indentation

-- Search
opt.ignorecase = true
opt.smartcase = true
opt.incsearch = true

-- Behavior
opt.mouse = "a"
opt.clipboard = "unnamedplus"
opt.undofile = true
opt.updatetime = 250 -- faster CursorHold events (diagnostics, etc.)
opt.timeoutlen = 400
opt.completeopt = { "menu", "menuone", "noselect" }
opt.wrap = false

-- Diagnostics look/feel (warnings & errors, per-severity icons)
vim.diagnostic.config({
  virtual_text = { spacing = 2, prefix = "●" },
  signs = {
    text = {
      [vim.diagnostic.severity.ERROR] = "✘",
      [vim.diagnostic.severity.WARN] = "▲",
      [vim.diagnostic.severity.INFO] = "ℹ",
      [vim.diagnostic.severity.HINT] = "➤",
    },
  },
  underline = true,
  update_in_insert = false,
  severity_sort = true,
  float = { border = "rounded", source = true },
})
