"============"
" FORMATTING "
"============"
set smarttab
set tabstop=4
set shiftwidth=4
set expandtab
set ai " Auto Indent
set si " Smart Indent

let g:rustfmt_autosave = 1

"===="
" UI "
"===="

"syntax highlighting
syntax enable

"searching
set hlsearch
set incsearch

"colour scheme
silent! colorscheme industry
set background=dark
set t_Co=256
highlight Normal ctermbg=NONE
highlight nonText ctermbg=NONE

"command area
set cmdheight=2

"line numbers
set number relativenumber

"backspace
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

"menu
set wildmenu
set wildignore=*.o,*~,*.pyc
if has("win16") || has("win32")
    set wildignore+=*/.git/*,*/.hg/*,*/.svn/*,*/.DS_Store
else
    set wildignore+=.git\*,.hg\*,.svn\*
endif

"============"
" FILE TYPES "
"============"
au BufNewFile,BufRead *.groovy  setf groovy
au BufNewFile,BufRead *.gradle  setf groovy

"=========="
" COMMANDS "
"=========="

function s:PrettyBox(val)
    if &filetype == ""
        let com_ft = ""
    else
        let com_ft = "--" . &filetype . " "
    endif
    let com_msg = system("prettybox " . com_ft . a:val . " 2>&1")
    call append(line('.'), split(com_msg, '\v\n'))
endfunction

command! -n=? Comment :call s:PrettyBox('<args>')

"========"
" VUNDLE "
"========"
set nocompatible
filetype off
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'gmarik/Vundle.vim'
Plugin 'rust-lang/rust.vim'
Plugin 'souffle-lang/souffle.vim'
Bundle 'takac/vim-hardtime'
Plugin 'Valloric/YouCompleteMe'
" Plugin 'vtreeexplorer'
call vundle#end() " All of your Plugins must be added before this line
filetype plugin indent on
"filetype plugin on

"==============="
" YOUCOMPLETEME "
"==============="
"let g:ycm_filetype_whitelist = { 'cpp':1, 'c':1 }
let g:ycm_filetype_blacklist = {'tex':1}
let g:ycm_enable_diagnostic_signs = 0
let g:ycm_autoclose_preview_window_after_insertion = 1
let g:ycm_extra_conf_globlist = ['./*','../*','../../*','!*']

"=========="
" HARDTIME "
"=========="
let g:hardtime_default_on = 1
let g:hardtime_allow_different_key=1
noremap <Up>    <esc>
noremap <Down>  <esc>
noremap <Left>  <esc>
noremap <Right> <esc>

"========="
" KEYMAPS "
"========="
let mapleader = ","
nnoremap <leader>w :w!<cr>
nnoremap <leader>q :q<cr>
nnoremap <leader>f :set filetype?<cr>
nnoremap <leader>p gqip

nnoremap <leader>d :Ex<cr>
nnoremap <leader>h :split<cr>
nnoremap <leader>v :vsplit<cr>

"ycm completion
nnoremap <leader>g :YcmCompleter GoTo<CR>

