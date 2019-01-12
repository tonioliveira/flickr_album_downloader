#!/usr/bin/env python

import os
from lxml import etree
import flickrapi
import urllib.request as req

api_key = u'f3240021b1b9d3576af8187882bc62bf' #obter no flickr a chave e o secret
api_secret = u'947c54b6eeac8fab'

my_user_id= '57527070@N06' #id de usuario (dono do album)
my_photoset_id = '72157655133305654' #id do album

flickr = flickrapi.FlickrAPI(api_key, api_secret)
flickr.authenticate_via_browser(perms='read')

#cria pasta para o album

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

#dowload de album completo

def original_secret(f_id): #obtem o secret original da foto
    photo_infos = flickr.photos.getInfo(photo_id = f_id)

    for e in photo_infos.iter('photo'):
        print('==>', e.attrib['originalsecret'])
        f = e.attrib['originalsecret']
    return f

photos_album = flickr.photosets.getPhotos(photoset_id = my_photoset_id, user_id = my_user_id)

createFolder('./%s/' % (my_photoset_id))

for f in photos_album.iter('photo'):
    farm_id = f.attrib['farm']
    server_id = f.attrib['server']
    ph_id = f.attrib['id']
    #ph_secret = f.attrib['secret']
    ph_info = ph_id
    ph_secret = original_secret(ph_id)
    #para tamanho da foto, final do link: original ('o_d'), large ('h_d'), medium ('z_d'), small ('m_d'), square ('q_d')
    photo_url = "https://farm%s.staticflickr.com/%s/%s_%s_o_d.jpg" % (farm_id, server_id, ph_id, ph_secret)
    print (photo_url)
    name = '%s/%s.jpg' % (my_photoset_id, ph_id)
    req.urlretrieve(photo_url, name)
