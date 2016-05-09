function [ ocrText1, ocrText2 ] = detecttext( imgpath, x1, y1, x2, y2, x3, y3, x4, y4)
%DETECTTEXT Summary of this function goes here
%   Detailed explanation goes here
%   Contrast: 1 = dark text light background
%             -1 = light text dark background

%[fileparts(fileparts(mfilename('fullpath'))), '/PERSPECTIVE_CONTROL']
addpath([fileparts(mfilename('fullpath')), '/PERSPECTIVE_CONTROL']);
addpath([fileparts(mfilename('fullpath')), '/SWT']);

img = imread(imgpath);
[orig_height, orig_width, orig_depth] = size(img);
downsampleScale = max(floor(sqrt(orig_height*orig_width)/900), 1);
img = imresize(img, 1/downsampleScale);
[height, width, depth] = size(img);
X = ones(4,1) + (width - 1) * [x1; x2; x3; x4] .* ones(4,1);
Y = ones(4,1) + (height - 1) * [y1; y2; y3; y4] .* ones(4,1);
homogrifiedImage = homogrify( img, X, Y );
image = homogrifiedImage;

swtMap1 = swt(image,1);
[swtLabel1, numCC1] = swtlabel(swtMap1);
final1 = extractletters(swtMap1, swtLabel1, numCC1);
ocrAns1 = ocr(final1);
ocrText1 = ocrAns1.Text;


swtMap2 = swt(image,-1);
[swtLabel2, numCC2] = swtlabel(swtMap2);
final2 = extractletters(swtMap2, swtLabel2, numCC2);
ocrAns2 = ocr(final2);
ocrText2 = ocrAns2.Text;


end
