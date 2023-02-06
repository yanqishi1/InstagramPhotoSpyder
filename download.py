js = """
        _fetch = function(i,src){
          return fetch(src).then(function(response) {
            if(!response.ok) throw new Error("No image in the response");
            var headers = response.headers;
            var ct = headers.get('Content-Type');
            var contentType = 'image/png';
            if(ct !== null){
              contentType = ct.split(';')[0];
            }

            return response.blob().then(function(blob){
              return {
                'blob': blob,
                'mime': contentType,
                'i':i,
              };
            });
          });
        };

        _read = function(response){
          return new Promise(function(resolve, reject){
            var blob = new Blob([response.blob], {type : response.mime});
            var reader = new FileReader();
            reader.onload = function(e){
              resolve({'data':e.target.result, 'i':response.i});
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
        };

        _replace = function(){
            for (var i = 0, len = q.length; i < len; i++) {imgs[q[i].item].src = q[i].data;}
        }

        var q = [];
        var imgs = document.querySelectorAll('img');
        for (var i = 0, len = imgs.length; i < len; i++) {
                _fetch(i,imgs[i].src).then(_read).then(function(data){
            q.push({
              'data': data.data,
              'item': data.i,
            });
          });
            }
        setTimeout(_replace, 1000 );
        """

imgsrc = "data:image/png;base64,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"

import base64
def base64img2file(imgsrc: str):
    suffix = imgsrc.split(';')[0][11:]
    with open("demo."+suffix, 'wb') as f:
        f.write(base64.b64decode(imgsrc.split(',')[1]))

if __name__ == '__main__':
    base64img2file(imgsrc)