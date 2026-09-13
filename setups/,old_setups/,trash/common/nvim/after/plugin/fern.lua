--nnoremap <leader>f :Fern . -reveal=% -drawer -toggle<CR>

vim.keymap.set('n', '<leader>f', function()
    vim.g.color_freeze = true
    vim.cmd [[ Fern . -reveal=% -drawer -toggle ]]
end)
