-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here

-- Move blocks of text at a time
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- Let Ctrl-e and Ctrl-y move 3 lines at a time
vim.keymap.set("n", "<C-e>", "3<C-e>")
vim.keymap.set("n", "<C-y>", "3<C-y>")
vim.keymap.set("v", "<C-e>", "3<C-e>")
vim.keymap.set("v", "<C-y>", "3<C-y>")

-- Print current location
vim.keymap.set("n", "<Space>t", function()
  print(vim.api.nvim_buf_get_name(0))
end)
