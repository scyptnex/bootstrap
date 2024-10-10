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

"viewport
set scrolloff=5

"colour scheme
"silent! colorscheme industry
"set background=dark
"set t_Co=256
"highlight Normal ctermbg=NONE
"highlight nonText ctermbg=NONE

"command area
set cmdheight=2

"line numbers
set number relativenumber

"backspace
set backspace=eol,start,indent
set whichwrap+=<,>,h,l

"no folding
set nofoldenable

"dont try and keep modified buffers in the foreground
set hidden

"menu
set wildmenu " pops up a menu when you hit <tab>
set wildmode=list " only shows the completions, does not try to pick one
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

"========="
" PLUGINS "
"========="
set nocompatible
call plug#begin('~/soft')
Plug 'psf/black'
Plug 'rust-lang/rust.vim'
Plug 'souffle-lang/souffle.vim'
Plug 'junegunn/fzf'
Plug 'jremmen/vim-ripgrep'
if !has('nvim')
    Plug 'Valloric/YouCompleteMe'
endif
" Plugin 'gmarik/Vundle.vim'
" Bundle 'takac/vim-hardtime'
" Plugin 'vtreeexplorer'
call plug#end()

"==============="
" YOUCOMPLETEME "
"==============="
"let g:ycm_filetype_whitelist = { 'cpp':1, 'c':1 }
let g:ycm_filetype_blacklist = {'tex':1}
let g:ycm_enable_diagnostic_signs = 0
let g:ycm_autoclose_preview_window_after_insertion = 1
let g:ycm_extra_conf_globlist = ['./*','../*','../../*','!*']

"========="
" TRYHARD "
"========="
vnoremap <Up> <nop>
vnoremap <Down> <nop>
vnoremap <Left> <nop>
vnoremap <Right> <nop>
inoremap <Up> <nop>
inoremap <Down> <nop>
inoremap <Left> <nop>
inoremap <Right> <nop>
nnoremap <Up> <nop>
nnoremap <Down> <nop>
nnoremap <Left> <nop>
nnoremap <Right> <nop>

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

nnoremap <leader>sc :e %:p:s,_test.cpp$,_EXPAND_,:s,.h$,_EXPAND_,:s,.cpp$,_EXPAND_,:s,_EXPAND_$,.cpp,<cr>
nnoremap <leader>sh :e %:p:s,_test.cpp$,_EXPAND_,:s,.h$,_EXPAND_,:s,.cpp$,_EXPAND_,:s,_EXPAND_$,.h,<cr>
nnoremap <leader>st :e %:p:s,_test.cpp$,_EXPAND_,:s,.h$,_EXPAND_,:s,.cpp$,_EXPAND_,:s,_EXPAND_$,_test.cpp,<cr>

"ycm completion
nnoremap <leader>g :YcmCompleter GoTo<CR>

