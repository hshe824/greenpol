#find coordinates of celestial bodies

import sys
##sys.path.append('C:/users/labuser/anaconda/lib/site-packages')
from datetime import datetime
from astropy.coordinates import AltAz, Angle, EarthLocation, ICRS, SkyCoord, frame_transform_graph
from astropy import units as u
import ephem


def getlocation(LOCATION):
	#observation locations
	locations = dict(
          Barcroft  = EarthLocation( lat=Angle(37.5838176, 'deg'),
                                    lon=Angle(-118.2373297, 'deg'), 
                                    height=3800 * u.m),
          Greenland = EarthLocation( lat=Angle(72.5796, 'deg'), 
                                    lon=Angle(-38.4592, 'deg'),
                                    height=3200 * u.m),
          UCSB      = EarthLocation( lat=Angle(34.414, 'deg'),
                                    lon=Angle(-119.843, 'deg'),
                                    height=14 * u.m),
)

	return locations[LOCATION]

def radec_to_azel(RA, DEC, location):

  #always use current time
  #time = str(datetime.utcnow())
  time = '2017-07-19 21:07:29.862000'

  location = getlocation(location)

  #create ra dec sky object
  radec = SkyCoord(ra = RA, dec = DEC, frame = 'icrs', unit='deg')

  #convert from ra dec to az/el for pointing
  azel = radec.transform_to(AltAz(obstime = time, location = location))

  az = azel.az.deg
  el = azel.alt.deg

  return az, el

def azel_to_radec(AZ, EL, location):

  #always use current time
  #time = str(datetime.utcnow())
  time = '2017-07-19 21:07:29.862000'

  location = getlocation(location)

  #create ra dec sky object
  azel = SkyCoord(az = AZ, alt = EL, obstime = time, location = location, frame = 'altaz', unit='deg')

  #convert from ra dec to az/el for pointing
  radec = azel.icrs

  ra = radec.ra.deg
  dec = radec.dec.deg

  return ra, dec

def getpointing(LOCATION, CBODY):


  #celestial bodies
  cbodies = dict(
  	  Sun     = ephem.Sun(),
  	  Moon    = ephem.Moon(),
  	  Mercury = ephem.Mercury(),
      Venus   = ephem.Venus(),
      Mars    = ephem.Mars(),
      Jupiter = ephem.Jupiter(),
      Saturn  = ephem.Saturn(),
      Uranus  = ephem.Uranus(),
      Neptune = ephem.Neptune()
  )

  #observer location
  location = getlocation(LOCATION)

  #check if cbody is a specific sky location
  if not isinstance(CBODY, str):
    RA = CBODY[0]
    DEC = CBODY[1]

    az, el = radec_to_azel(RA, DEC, location)

    return az, el

  #current utc time
  time = str(datetime.utcnow())

  #celestial body of interest
  cbody = cbodies[CBODY]

  #this method take 2x as long and produces a slightly different azel, I am not sure which is more accurate
  '''
  ##########################
  #compute radec of body at current time
  cbody.compute(time)

  #create icrs object to convert to az el
  icrs = ICRS(ra = Angle(str(cbody.ra) + 'hours'), dec = Angle(str(cbody.dec) + 'degrees'))
  #print icrs.ra.deg, icrs.dec.deg
  #convert to altaz coordinates
  altaz = icrs.transform_to(AltAz(obstime=t, location=location))
  print altaz.az.deg, altaz.alt.deg
  #############################
  '''

  #set observer location and epoch
  obs = ephem.Observer()
  obs.lon, obs.lat = str(location.longitude.deg), str(location.latitude.deg)
  obs.elevation = float(str(location.height).split()[0])
  obs.date = time

  #compute celestial body az/el coordinates given observer spacetime coordiantes
  cbody.compute(obs)

  #convert azimuth to degrees
  az = str(cbody.az).split(':')
  az = [float(i) for i in az]
  az = (az[0] + az[1]/60. + az[2]/60./60.)

  #convert altitude to degrees
  alt = str(cbody.alt).split(':')
  alt = [float(i) for i in alt]
  alt = (alt[0] + alt[1]/60. + alt[2]/60./60.)

  #return azimuth and altitude of celestial body
  return az, alt

