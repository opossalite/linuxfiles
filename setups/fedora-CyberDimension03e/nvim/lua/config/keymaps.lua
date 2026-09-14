-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
--

-- Copy and paste from the system clipboard
vim.keymap.set({ "n", "v" }, "<leader>y", '"+y', { desc = "Yank to system clipboard" })
vim.keymap.set({ "n", "v" }, "<leader>p", '"+p', { desc = "Paste from system clipboard" })

-- Move blocks of text at a time
vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

-- Let Ctrl-e and Ctrl-y move 3 lines at a time
vim.keymap.set("n", "<C-e>", "3<C-e>")
vim.keymap.set("n", "<C-y>", "3<C-y>")
vim.keymap.set("v", "<C-e>", "3<C-e>")
vim.keymap.set("v", "<C-y>", "3<C-y>")

-- Recenter screen after using these commands
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

-- Reorder buffers
vim.keymap.set("n", "<C-[>", ":BufferLineMovePrev<CR>")
vim.keymap.set("n", "<C-]>", ":BufferLineMoveNext<CR>")

-- Print current location, find a way to print the whole thing
vim.keymap.set("n", "<Space>t", function()
  print(vim.api.nvim_buf_get_name(0))
end)

-- Delete without copying in visual mode
vim.keymap.set("v", "<BS>", '"_d', { desc = "Delete selection without copying" })
