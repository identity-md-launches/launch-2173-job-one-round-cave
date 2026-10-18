'use strict';
// Preserve all ancestral pixels outside the new, formerly empty patch.
const fs = require('node:fs');
const {decodePNG, encodePNG, preview} = require('./finish_wall.js');
const ancestor = decodePNG('artifacts/line-1/wall-v3.png');
const generated = decodePNG('artifacts/line-1/wall-v4.png');
if (ancestor.width !== 1254 || ancestor.height !== 1254 || generated.width !== 1254 || generated.height !== 1254 || generated.channels !== ancestor.channels) throw Error('unexpected image dimensions or channels');
const bounds = [803, 708, 987, 880];
const [left,top,right,bottom] = bounds;
const result = {...ancestor,pixels:Buffer.from(ancestor.pixels)};
let changed = 0;
for (let y=top; y<bottom; y++) for (let x=left; x<right; x++) {
  const blend = Math.min(1,(x-left)/10,(right-1-x)/10,(y-top)/10,(bottom-1-y)/10);
  const at = (y*ancestor.width+x)*ancestor.channels;
  for (let c=0;c<ancestor.channels;c++) result.pixels[at+c] = Math.round(ancestor.pixels[at+c]*(1-blend)+generated.pixels[at+c]*blend);
  if (!result.pixels.subarray(at,at+ancestor.channels).equals(ancestor.pixels.subarray(at,at+ancestor.channels))) changed++;
}
let outside = true;
for (let y=0; y<1254; y++) for(let x=0;x<1254;x++) {
  if(left<=x && x<right && top<=y && y<bottom) continue;
  const at=(y*1254+x)*ancestor.channels;
  if (!result.pixels.subarray(at,at+ancestor.channels).equals(ancestor.pixels.subarray(at,at+ancestor.channels))) outside=false;
}
if(!outside) throw Error('ancestor preservation failed');
fs.writeFileSync('artifacts/line-1/wall-v4.png',encodePNG(result));
const jpg=preview(result);
if(jpg.length>100000) throw Error('JPEG too large');
fs.writeFileSync('dist/line-1/24.jpg',jpg);
console.log(JSON.stringify({bounds,changed_pixels:changed,all_pixels_outside_identical:outside,preview_bytes:jpg.length}));
