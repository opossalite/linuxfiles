function! s:init_fern() abort
    nnoremap <buffer> <C-h> <C-w>h
    nnoremap <buffer> <C-l> <C-w>l
endfunction

augroup fern-custom
    autocmd! *
    autocmd FileType fern call s:init_fern()
augroup END

nnoremap <leader>f :Fern . -reveal=% -drawer -toggle<CR>

