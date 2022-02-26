#! /bin/sh

(  # avoid having to cd back by using ( subshell )
cd 'arc-pdf-ui' || exit
npm install -g npm@latest && npm install
)

npx arc sandbox