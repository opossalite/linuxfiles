" To open lf when vim load a directory
"if exists('g:lf_replace_netrw') && g:lf_replace_netrw
"  augroup ReplaceNetrwByLfVim
"    autocmd VimEnter * silent! autocmd! FileExplorer
"    autocmd BufEnter * let s:buf_path = expand("%") | if isdirectory(s:buf_path) | bdelete! | call timer_start(100, {->OpenLfIn(s:buf_path, s:default_edit_cmd)}) | endif
"  augroup END
"endif
