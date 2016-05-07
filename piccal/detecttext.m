function [ ocrText ] = detecttext( img, contrast)
%DETECTTEXT Summary of this function goes here
%   Detailed explanation goes here
%   Contrast: 1 = dark text light background
%             -1 = light text dark background

%image = imread(imName);
image = imresize(img, 0.25);
swtMap = swt(image,contrast);
[swtLabel numCC] = swtlabel(swtMap);
final = extractletters(swtMap, swtLabel, numCC);
ocrAns = ocr(final);
ocrText = ocrAns.Text;


end