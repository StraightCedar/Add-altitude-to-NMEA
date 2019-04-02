# Add-altitude-to-NMEA
Add or update altitude data to NMEA.
For example, SONY Action-CAM does't have any altitude data in GPS information in MOFF file.
This program gets altitude data from Technical Report of the Geospatial Information Authority of Japan site,
and add then into NMEA data.
To erxtract and create NMEA data file from SONY Action-CAM MOFF file, please use my NMEA-Extractor.
To use it with other than "Technical Report of the Geospatial Information Authority of Japan" site information,
change "GetAltitude" function, which referes the WEB-API using latitude and longitude to get altitude.

NMEA データへ高度情報を追加します。もしくは高度情報を更新します。
例えば SONY アクションカムの GPS データ (MOFF ファイル内にあります) は高度データを持っていません。
このプログラムは、国土地理院のサイトから高度データを取得し、NMEA データへ追加します。
NMEA データを MOFF ファイルから抽出するには、私の NMEA-Extractor をご利用ください。
国土地理院以外の地図情報を利用するには、WEB-API で緯度経度から高度情報を参照している部分
(GetAltitude 関数) を修正してください。


