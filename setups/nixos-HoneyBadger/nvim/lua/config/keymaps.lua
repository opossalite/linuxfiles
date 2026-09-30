local map = vim.keymap.set

-- Basic quality-of-life
map("i", "jk", "<Esc>", { desc = "Exit insert mode" })
map("n", "<Esc>", "<cmd>nohlsearch<CR>", { desc = "Clear search highlight" })
map("n", "<leader>w", "<cmd>w<CR>", { desc = "Save file" })

-- Window navigation
map("n", "<C-h>", "<C-w>h", { desc = "Go to left window" })
map("n", "<C-j>", "<C-w>j", { desc = "Go to lower window" })
map("n", "<C-k>", "<C-w>k", { desc = "Go to upper window" })
map("n", "<C-l>", "<C-w>l", { desc = "Go to right window" })

-- File tree: mapped to BOTH <leader>e and <leader>f, your choice which to use.
-- (Actual toggle command is wired up in lua/plugins/neotree.lua once the plugin loads.)

-- Shift+L: show diagnostics (errors/warnings) for the current line in a float.
-- Shift+K is LSP hover (type info, docs) -- wired up per-buffer in lsp.lua's
-- LspAttach autocmd, since it only makes sense once a language server attaches.
-- Note: this overrides the built-in K (keywordprg/man lookup) and L (bottom-of-
-- screen motion), per your preference.
map("n", "L", vim.diagnostic.open_float, { desc = "Show diagnostics at cursor" })

-- Same diagnostic float, kept as a leader alias too.
map("n", "<leader>d", vim.diagnostic.open_float, { desc = "Show line diagnostics" })
map("n", "<leader>q", vim.diagnostic.setloclist, { desc = "Diagnostics to location list" })
