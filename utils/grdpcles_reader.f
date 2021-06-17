c ###################################################################
c WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
c This version of Aires has been compiled with GrdpclesFormat=3
c ###################################################################
c Read Aires grdpcles files and creates two text files containing:
c (1) electromagnetic particle densities in an xy grid
c (2) muonic particle densities in an xy grid 
c ###################################################################
      program read_grdpcles 

      save

      parameter(nxmax=10000,nymax=10000)

      integer i,irc,channel,nshowers,n,code
      common/showers/nshowers

c Aires
      integer indata(30), intdata(30)
      double precision fldata(30), realdata(30)
      character*80 filename,dir,fileoutput

c Map parameters
      real xsize,ysize,step,area_cell 
      real xmin,xmax,ymin,ymax
      common/map/xmin,xmax,ymin,ymax,area_cell
      integer nx,ny
      common/map2/nx,ny
      common/map3/step

      real n_out,e_out
      common/outside/n_out,e_out
      
      integer icode, iener, idist, iphi, iweig, iux, iuy

c Shower properties
      real energy,zenith,azimuth,secth

c Particle properties
      real E,KinE,wei,r,phi,zenp
      real ux,uy,uz,umod2
      real last_had_int,creation_depth
      real arrival_time
      real KthmuCher,KthCher,EthgCher
      real Eth_g,Kth_e,Kth_mu

c Output
      real n_el,n_ph,n_mu
      real e_el,e_ph,e_mu
      common/particles/n_el,n_ph,n_mu,e_el,e_ph,e_mu

c Densities
      real w_em,w_mu
      common/densities/w_em(nxmax,nymax),w_mu(nxmax,nymax)

      real pi,pihalfs

      real xm_e,xm_mu
      common/mass/xm_e,xm_mu

      n=1

      n_ph=0. 
      e_ph=0. 

      n_el=0.
      e_el=0.

      n_mu=0.
      e_mu=0.

      n_out=0.
      e_out=0.

! ----------------------------
      pi=4.d0*atan(1.d0)
      pihalfs=0.5d0*pi
! ----------------------------
! Electron mass [GeV]
      xm_e=0.000511
! Muon mass [GeV]
      xm_mu=0.1056583
! ----------------------------
! Cherenkov thresholds in water of refractive index 1.33
! (kinetic energy in GeV)
! Muons
      KthmuCher = 0.0546
! Electrons and positrons
      KtheCher = 0.000264
! Photons
      EthgCher = 2.*xm_e + KtheCher

! Particle thresholds
      Eth_g = EthgCher
      Kth_e = KtheCher
      Kth_mu = KthmuCher
! ----------------------------


! ----------------------------
c Inputs
      write(*,*) 'Aires grdpcles filename'
      read (*,20) filename
      write(*,*) filename
20    format(a80)

      read (*,*) fileoutput 
      open(unit=99,file=fileoutput,status='unknown')

      dir='./'

      write(*,*) 'Grid size along x and y (m)'
      read (*,*) xsize,ysize 
      write(*,*) xsize,ysize 

      write(*,*) 'Step (m)'
      read (*,*) step 
      write (*,*) step 

      write(*,*) 'Number of showers'
      read (*,*) nshowers
      write (*,*) nshowers

      ! grid function prints xmin,xmax,ymin,ymax,nx,ny
      call grid(xsize,ysize,step,xmin,xmax,ymin,ymax,nx,ny,area_cell)

c      write(*,*) xmin,xmax,ymin,ymax,nx,ny,area_cell

c ####################################
c Read data from .grdpcles AIRES files
c See Chapter 4 in Aires manual for more info
c See Tables 4.1 to 4.6 in Aires manual for info on the fields in grdpcles files
c See Table 4.7 in Aires manual for info on particle data codes
c ####################################
      call ciorinit (0,1,0,irc)
      call opencrofile (dir,filename,0,10,4,channel,irc) 
      call crofileinfo(channel, 0, 4, irc)

!      icode = crofieldindex(channel, 0, 'Particle code', 4, datype, irc)
!      iener = crofieldindex(channel, 0, 'Energy', 4, datype, irc)
!      idist = crofieldindex(channel, 0, 'Distance from the core', 4, datype, irc)
!      iphi  = crofieldindex(channel, 0, 'Ground plane polar angle', 4, datype, irc)
!      iweig = crofieldindex(channel, 0, 'Particle weight', 4, datype, irc)
!      iux   = crofieldindex(channel, 0, 'Direction of motion (x component)', 4, datype, irc)
!      iuy   = crofieldindex(channel, 0, 'Direction of motion (y component)', 4, datype, irc)
      
10    okflag=getcrorecord(channel,indata,fldata,altrec,0,irc)
c      if(irc.ne.0) write(*,*) irc
       
! ------------------------------
! Beginning of shower record
! ------------------------------
      if (irc.eq.1) then

         energy=(10.**(fldata(1)))*1.e9      ! shower energy eV
         zenith=fldata(2)                    ! shower zenith angle (deg)
         azimuth=fldata(3)                   ! shower azimuth angle (deg)
         xfirst=fldata(5)                    ! vertical depth of 1st interaction (g/cm^2) 

         write(*,*) 'Shower energy (eV) ',energy
         write(*,*) 'Shower zenith angle (deg) ',zenith
         write(*,*) 'Shower azimuthal angle (deg) ',azimuth
         write(*,*) 'First interaction depth (g/cm^2) ',xfirst

! ------------------------------
! Regular particle entry
! ------------------------------
! Read:
! photons (1)
! e+ (2), e- (-2)
! mu+ (3), mu-(-3) 
! ------------------------------
      else if( (irc.eq.0) .and.
     &  (abs(indata(1)).ge.1) .and.
     &  (abs(indata(1)).le.3) ) then
          
          code=indata(1)

          KinE=10.**(fldata(3)) !iener))   ! Kinetic energy (GeV)
          r=10.**(fldata(4)) !idist))      ! Distance to core on ground (m) 
          phi=fldata(5) !iphi)           ! Polar angle on ground (rad)
          wei=fldata(9) !iweig)           ! Particle weight

          ux=fldata(6) !iux)            ! p_x/|p| at arrival at ground
          uy=fldata(7) !iuy)            ! p_y/|p| at arrival at ground
          umod2=ux*ux+uy*uy     
          if (umod2.gt.1.0) umod2=1. 
          uz=sqrt(1.-umod2)       ! p_z
          if (abs(uz).gt.1.0) uz=sign(1.,uz)
          zenp=acos(uz)           ! arrival angle (rad)

! Elliminate particles hitting the ground at >= 90 deg. if there is any 
!          if (zenp.ge.pihalfs) then 
!            goto 10
!          end if

          creation_depth=fldata(10)      ! Particle creation depth (g/cm^2)
          last_had_int=fldata(11)        ! Depth of last hadronic interaction 
                                        ! before particle creation (g/cm^2)
          arrival_time=real(fldata(8))  ! Arrival time (ns)

!          write(*,*) '=============================='
!          write(*,*) 'Particle code = ',code
!          write(*,*) 'Kinetic Energy (GeV) = ',KinE
!          write(*,*) 'Distance to core (m) = ',r
!          write(*,*) 'Ground plane polar angle (deg) = ',phi*180./3.141592
!          write(*,*) 'Particle weight = ',wei
!          write(*,*) 'ux, uy = ',ux,uy
!          write(*,*) 'angle 1 = ',atan(uy/ux)*180./pi
!          write(*,*) 'zenp (deg) = ',zenp*180./pi
          
          write(99,*) code, r, phi, ux, uy, KinE  ! Write azimuth angle in file

! Only gammas above kinetic threshold in water
          if (abs(code).eq.1 .and. (KinE.lt.Eth_g)) goto 10
! Only e+, e- above kinetic threshold in water
          if (abs(code).eq.2 .and. (KinE.lt.Kth_e)) goto 10
! Only mu+, mu- above kinetic threshold in water
          if (abs(code).eq.3 .and. (KinE.lt.Kth_mu)) goto 10

c          write(*,*) code,KinE,r,zenp,phi,wei,ux,uy,uz,
c     #               arrival_time

! ###############################################
! Put particle in its corresponding bin on ground 
! ###############################################

      call create_map(code,KinE,r,zenp,phi,wei,
     &                zenith,azimuth,ux,uy,uz,
     &                arrival_time)


! ------------------------------
! End of shower
! ------------------------------
      else if (irc.eq.2) then  ! End of shower record

        n=n+1

        if (n.gt.nshowers)  goto 30
        write(*,*) '--------------------------------------------'
        write(*,*) 'n=',n

      endif

      goto 10

30    continue

      write(*,*) 'End reading file'

c -----------------------------------------------
c Write particle density map
c -----------------------------------------------

      write(*,*) 'xmax (m) = ',xmax
      write(*,*) 'xmin (m) = ',xmin
      write(*,*) 'ymax (m) = ',ymax
      write(*,*) 'ymin (m) = ',ymin
      write(*,*) 'step (m) = ',step
      write(*,*) 'area cell (m^2) = ',area_cell
      write(*,*) 'particles reaching ground (#) = ',fldata(4)
      write(*,*) 'particles reaching grid (#)   = ',fldata(7)

!      do ix=1,nx
!        do iy=1,ny
!          x=xmin+ix*step
!          y=ymin+iy*step
!          write(99,*) x,y,
!     #       w_em(ix,iy)/area_cell/float(nshowers),
!     #       w_mu(ix,iy)/area_cell/float(nshowers)
!        end do
!      end do

      write(*,*) '--------------------------------------------'
      write(*,22) 'Avrg. number of e+,e-    ',n_el/float(nshowers) 
      write(*,22) 'Avrg. E of e+,e- (MeV)   ',e_el*1.e-3/float(nshowers)
      write(*,*) '--------------------------------------------'
      write(*,22) 'Avrg. number of photons  ',n_ph/float(nshowers) 
      write(*,22) 'Avrg. E of photons (MeV) ',e_ph*1.e-3/float(nshowers)
      write(*,*) '--------------------------------------------'
      write(*,22) 'Avrg. number of muons    ',n_mu/float(nshowers) 
      write(*,22) 'Avrg. E of muons (MeV)   ',e_mu*1.e-3/float(nshowers)
      write(*,*) '--------------------------------------------'
      write(*,22) 'Avrg. particles out grid ',n_out/float(nshowers) 
      write(*,22) 'Avrg. E out grid (MeV)   ',e_out/float(nshowers) 
      write(*,*) '--------------------------------------------'
22    format(A26,1P,1E14.6)

      end

c ###################################################################
c All distances in m
c ###################################################################
      subroutine 
     #grid(xsize,ysize,step,xmin,xmax,ymin,ymax,nx,ny,area_cell)
      save

      parameter(nxmax=10000,nymax=10000)

      integer nx,ny

      real xmin,xmax,ymin,ymax
      real xsize,ysize,step
      real area_cell

c Number of bins in x and y
      nx=int(xsize/step)
      ny=int(ysize/step)

      if (nx.gt.nxmax) write(*,*) "Warning: nx > ",nxmax
      if (ny.gt.nymax) write(*,*) "Warning: ny > ",nymax

      xmin=-(step*nx)/2.
      xmax=(step*nx)/2.

      ymin=-(step*nx)/2.
      ymax=(step*nx)/2.

      write(*,*) xmin,xmax,ymin,ymax
      write(*,*) nx,ny

      area_cell=step*step    ! m^2
     
      return
      end

c ###################################################################
      subroutine 
     & create_map(code,KinE,r,zenp,phi,wei,
     &  zenith,azimuth,ux,uy,uz,arrival_t)

      save

      parameter(nxmax=10000,nymax=10000)

      integer code,n

      real xmin,xmax,ymin,ymax,area_cell
      common/map/xmin,xmax,ymin,ymax,area_cell
      integer nx,ny
      common/map2/nx,ny
      common/map3/step

      real n_out,e_out
      common/outside/n_out,e_out

      real w_em,w_mu
      common/densities/w_em(nxmax,nymax),w_mu(nxmax,nymax)

      real arrival_t 
      real ux,uy,uz
      real ushx,ushy,ushz

      real n_el,n_ph,n_mu
      real e_el,e_ph,e_mu
      common/particles/n_el,n_ph,n_mu,e_el,e_ph,e_mu

      real phi
      real zenp,zenpdeg
      real znth,phinew,phinewdeg,angle
      real zenith,zenrad,azimuth,azirad
      real wei
      real xp,yp,xnew,ynew,r,rnew

      real E,KinE

      double precision pi,pihalfs

      common/mass/xm_e,xm_mu

! ----------------------------
      pi=4.d0*atan(1.d0)
      pihalfs=0.5d0*pi
! ----------------------------
      zenpdeg=180.*zenp/pi

! now angles in radians
      zenrad=pi*zenith/180.0
      azirad=pi*azimuth/180.0

! Unitary vector in the direction of motion of the shower
      ushx=sin(zenrad)*cos(azirad)
      ushy=sin(zenrad)*sin(azirad)
      ushz=cos(zenrad)

! change from Aires to Auger coord. system.
!      phi=phi+pi/2.

! coordinates on ground
      xp=r*cos(phi)
      yp=r*sin(phi)

! Align x axis so that is parallel to the projection of
! shower axis 
        xnew=xp*cos(azirad)+yp*sin(azirad)
        ynew=-xp*sin(azirad)+yp*cos(azirad)
!        xnew=xp
!        ynew=yp

      rnew=sqrt(xnew**2+ynew**2)

! -----------------------------
! Particle and energy densities 
! -----------------------------
         if ((xnew.lt.xmin).or.(xnew.gt.xmax)) then
           n_out=n_out+wei
           if (code.eq.1) e_out=e_out+KinE*wei
           if (abs(code).eq.2) e_out=e_out+(KinE+xm_e)*wei
           goto 111
         end if 

         if ((ynew.lt.ymin).or.(ynew.gt.ymax)) then
           n_out=n_out+wei
           if (abs(code).eq.3) e_out=e_out+(KinE+xm_mu)*wei
           goto 111
         end if 

! Find bin where particle is found
         ix = int((xnew-xmin)/step)+1
         iy = int((ynew-ymin)/step)+1
c         write(*,*) xnew,ynew,xmin,ymin,step,ix,iy,code,wei
! -------------------------------------------------------------------------
      if ((abs(code).eq.1).or.(abs(code).eq.2)) then  ! Gammas, e+, e-

         if (code.eq.1) then          ! photons 
           E = KinE
           n_ph = n_ph + wei
           e_ph = e_ph + wei*E
         end if

         if (abs(code).eq.2) then     ! e+, e-
           E = xm_e + KinE
           n_el = n_el + wei
           e_el = e_el + wei*E
         end if

         w_em(ix,iy)=w_em(ix,iy)+wei   ! photons, e+, e-

      else if (abs(code).eq.3) then     ! mu+, mu-

         E = xm_mu + KinE
         n_mu = n_mu + wei
         e_mu = e_mu + wei*E

         w_mu(ix,iy)=w_mu(ix,iy)+wei

      end if
! -------------------------------------------------------------------------

111   continue

      return

      end 
