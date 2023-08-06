# mdbridge

markdown extension for writing bridge article, a fast way to write qualified articles from existing xinrui url and bbo lin url

````
<pre lang="bridge">
http://www.xinruibridge.com/deallog/DealLog.html?bidlog=P;1N,P,3N,P;P,P&playlog=W:6H,TH,KH,5H;E:9H,AH,3H,JH;S:TD,8D,2D,6D;S:KD,QH,5D,3D;S:7D,4C,JD,4D;N:QD,9D,2C,8S;N:AD,3S,5S,6S;N:KC,6C,3C,8C;N:2S,4S,KS,AS;W:8H,9C,2H,5C;W:7H,TS,9S,7C;W:4H,TC,7S,JS;W:JC,QS,QC,AC;&deal=9743.K92.9643.Q6%20KJ5.A5.KT7.A7532%20A86.Q87643.8.J84%20QT2.JT.AQJ52.KT9&vul=None&dealer=E&contract=3N&declarer=S&wintrick=8&score=-50&str=%E5%9B%A2%E4%BD%93%E8%B5%9B%20%E7%AC%AC10%E8%BD%AE%20%E7%89%8C%E5%8F%B7%
https://www.bridgebase.com/myhands/fetchlin.php?id=765880487&when_played=1610464081
deal
auction
</pre>
````

![](snapshot.png)

## Key features (beta release)

* support xinrui url, bbo lin url (bbo soon)
* generate well tuned latex/html bridge layout (card diagram) 
* generate all kinds of ebook (`.pdf`/`.mobi`/`.epub`/`.html`/`.latex`) with related toolchains (`pandoc`,`multimarkdown`) 

# Samples

* Ramsey's article for xinrui bridge (Chinese), see [ramsey.md](https://xrgopher.gitlab.io/mdbridge/ramsey.md) and [ramsey.pdf](https://xrgopher.gitlab.io/mdbridge/ramsey.pdf)

# How to use it

Generally, follow below steps 

* write it in special format with markdown
* use `mdbridge` tool to generate intermediate markdown file
* use `multimarkdown` or `pandoc` to generate related format files
* generate final ebook

See below

````
# sample.md
<pre lang="bridge">
http://www.xinruibridge.com/deallog/DealLog.html?bidlog=P;1N,P,3N,P;P,P&playlog=W:6H,TH,KH,5H;E:9H,AH,3H,JH;S:TD,8D,2D,6D;S:KD,QH,5D,3D;S:7D,4C,JD,4D;N:QD,9D,2C,8S;N:AD,3S,5S,6S;N:KC,6C,3C,8C;N:2S,4S,KS,AS;W:8H,9C,2H,5C;W:7H,TS,9S,7C;W:4H,TC,7S,JS;W:JC,QS,QC,AC;&deal=9743.K92.9643.Q6%20KJ5.A5.KT7.A7532%20A86.Q87643.8.J84%20QT2.JT.AQJ52.KT9&vul=None&dealer=E&contract=3N&declarer=S&wintrick=8&score=-50&str=%E5%9B%A2%E4%BD%93%E8%B5%9B%20%E7%AC%AC10%E8%BD%AE%20%E7%89%8C%E5%8F%B7%2014/16&dealid=794018966&pbnid=221536004
deal|cards=NS|ul="<str>"|ll=<str>|ur=<str>`
</pre>
$ pip install mdbridge
$ mdbridge2latex sample.md
sample.bridge-tex is created
$ multimarkdown -t latex meta.txt sample.bridge-tex -o sample.tex
$ xelatex article.tex # article.tex is not released yet
````

The complete guideline will be released soon.

## markdown format

### define the deal from url first

<pre lang="bridge">
http://www.xinruibridge.com/deallog/DealLog.html?bidlog=P,2N,P%3B3C,P,3N,P%3B6N,P,P,P%3B&playlog=E:KD,3D,4D,JD%3BE:2D,5D,7D,AD%3BN:JS,6S,5S,8S%3BN:KS,4S,7S,2S%3BN:3S,TS,AS,8H%3BS:QS,TD,4C,9S%3BS:KH,JH,4H,2H%3BS:AH,TH,9H,3H%3BS:QH,9D,8C,5H%3BS:2C,JC,QC,6C%3BN:KC,9C,6D,5C%3BN:AC,7H,6H,3C%3BN:7C,QD,8D,TC%3B&deal=82.JT8.T974.JT53%20KJ3.94.AJ.AKQ874%20T964.7532.KQ2.96%20AQ75.AKQ6.8653.2&vul=All&dealer=W&contract=6N&declarer=N&wintrick=11&score=-100&str=%E7%BE%A4%E7%BB%84IMP%E8%B5%9B%2020201209%20%E7%89%8C%E5%8F%B7%204/8&dealid=995050099&pbnid=345464272
auction
</pre>

### customize the deal

`deal|cards=NS|ul="<str>"|ll=<str>|ur=<str>`

Two-Hand Diagram

<pre lang="bridge">
deal|cards=NS
</pre>

All-Hands Diagram

<pre lang="bridge">
deal
</pre>

Partial deal

<pre lang="bridge">
deal=.xxxx..xxx&.T4.A.AK87&-&.AKQ6.865.
</pre>

Partial deal with extra information

<pre lang="bridge">
deal=.xxxx..xxx&.94.A.AK87&-&.AKQ6.865.|ll="NS 4/12&EW 0"|ur="match 4/8"
</pre>

# Collaborator

* Ramsey @ xinrui : mainly for latex template and tune the card diagrams

# Reference

* http://www.rpbridge.net/7z69.htm