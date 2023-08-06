import os
import sys
from functools import reduce
from os.path import join as opj
from distutils.core import setup, Extension
from Cython.Distutils import build_ext

__package_name__ = 'gsrp5webserver'
__package_file__ = 'gsrp5-webserver'

install_requires = ['tornado']

modules = []
package_data = {__package_name__:['*.wsgi','*.crt','*.key','certs/*.crt','certs/*.key']}
data_files = [('/lib/systemd/system',[opj(__package_name__,'conf', 'gsrp5-webserver.service')]),('/etc/gsrp5-webserver.d',[opj(__package_name__, 'conf', 'webserver.conf')])]

for lang in os.listdir(opj(__package_name__,'locale')):
	data_files.append((os.path.join(sys.prefix,'share', 'locale', lang, 'LC_MESSAGES'),[os.path.join(__package_name__,'locale', lang, 'LC_MESSAGES','gsrp5webserver.mo')]))

for d in os.walk(__package_name__):
	l = list(map(lambda x:x[:-2],list(filter(lambda x: x[0] != '.' and x[-2:]=='.c',d[2]))))
	if len(l) > 0:
		a=list(map(lambda x:opj(d[0],x), l ))
		for n in a:
			n1 = n.split('/')[-1:][0]
			modules.append(Extension('%s' % (n,), sources = ['%s' % (n + '.c')],language='clang'))

for sd in ('lib','static','web'):
	for d in os.walk(opj('gsrp5webserver',sd)):
		l = list(map(lambda x:x,list(filter(lambda x: not (x[-3:] in ('.py','.so') or x[-4:] == '.pyc'),d[2]))))
		if len(l) > 0:
			a=list(map(lambda x:opj(d[0],x), l ))
			for n in a:
				data_files.append((opj(sys.base_prefix,'lib64','python'+('%s.%s') % (sys.version_info.major,sys.version_info.minor),'site-packages',d[0]),[n]))

#print('data-file:',data_files)

setup (name = __package_file__, package_data = package_data, data_files = data_files, scripts = [__package_name__ + '/script/gsrp5-webserver'], packages = [__package_name__],version = '1.0.1', install_requires=install_requires,description = 'Global System Resource Planing',long_description = 'GSRP Tornado Web Server for access in browser', author='Nikolay Chesnokov', author_email='nikolaychesnokov@gmail.com' , url='http://www.gsrp.org', license='AGPL-3',cmdclass = { 'build_ext': build_ext },ext_modules = modules)
