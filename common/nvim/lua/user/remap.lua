vim.g.mapleader = " "
vim.keymap.set("n", "<leader>pv", vim.cmd.Ex)

vim.keymap.set("n", "<C-e>", "3<C-e>")
vim.keymap.set("n", "<C-y>", "3<C-y>")
vim.keymap.set("v", "<C-e>", "3<C-e>")
vim.keymap.set("v", "<C-y>", "3<C-y>")

vim.keymap.set("v", "J", ":m '>+1<CR>gv=gv")
vim.keymap.set("v", "K", ":m '<-2<CR>gv=gv")

vim.keymap.set("n", "J", "mzJ'z")
vim.keymap.set("n", "<C-d>", "<C-d>zz")
vim.keymap.set("n", "<C-u>", "<C-u>zz")
vim.keymap.set("n", "n", "nzzzv")
vim.keymap.set("n", "N", "Nzzzv")

vim.keymap.set("x", "<leader>p", "\"_dP")

vim.keymap.set("n", "<leader>y", "\"+y")
vim.keymap.set("v", "<leader>y", "\"+y")
vim.keymap.set("n", "<leader>Y", "\"+Y")
vim.keymap.set("n", "<leader>pp", "\"+p")

vim.keymap.set("i", "<C-c>", "<Esc>")

vim.keymap.set("n", "Q", "<nop>")

vim.keymap.set('n', '<C-h>', '<C-w>h')
vim.keymap.set('n', '<C-j>', '<C-w>j')
vim.keymap.set('n', '<C-k>', '<C-w>k')
vim.keymap.set('n', '<C-l>', '<C-w>l')

vim.g.wrap = false
vim.keymap.set('n', 'L', function()
    if vim.g.wrap == true then
        vim.cmd [[ set nowrap ]]
        vim.cmd [[ nnoremap <expr> k (v:count == 0 ? 'gk' : 'k') ]]
        vim.cmd [[ nnoremap <expr> j (v:count == 0 ? 'gj' : 'j') ]]
        vim.g.wrap = false
    else
        vim.cmd [[ set wrap ]]
        vim.g.wrap = true
    end
end)

vim.keymap.set('n', 'Y', function()
    print(vim.api.nvim_buf_get_name(0))
end)


