pyinstaller Omegar-Toolbox.spec --distpath build --workpath build/temp
cd build
rm -r temp
mv Omegar-Toolbox Omegar-Toolbox-Linux
