
subroutine read_dcd(fname, nstr, natom, box, x, y, z)
  implicit none

  ! input variables
  character(len=256), intent(in) :: fname
  integer, intent(in) :: nstr, natom

  ! output variables
  real(kind=8), dimension(1:nstr, 1:3), intent(out) :: box
  real, dimension(1:nstr, 1:natom), intent(out) :: x, y, z

  !f2py intent(out) box
  !f2py intent(out) x
  !f2py intent(out) y
  !f2py intent(out) z

  ! temporary variables
  character(len=80), dimension(1:2) :: title
  character(len=4) :: dcdhdr
  integer, dimension(1:9) :: dumi
  real :: dumr
  real(kind=8) :: dumr8
  integer :: nstr0, ntitle, natom0, i, j

  ! open dcd file
  open(24, file=trim(fname), status='old', form='unformatted')

  ! header
  read(24) dcdhdr, nstr0, dumi(1:8), dumr, dumi(1:9)
  if(nstr /= nstr0) then
   print*, 'Error: unexpected number of structures.'
   stop
  end if
  read(24) ntitle, title(1:ntitle)
  if(ntitle /= 2) then
   print*, 'Error: ntitle /= 2.'
   stop
  end if
  read(24) natom0
  if(natom /= natom0) then
   print*, 'Error: unexpected number of atoms.'
   stop
  end if

  ! loop over all structures
  do i = 1, nstr, 1
   ! read in box information
   read(24) box(i,1), dumr8, box(i, 2), dumr8, dumr8, box(i, 3)

   ! read in coordinates
   read(24) x(i, 1:natom)
   read(24) y(i, 1:natom)
   read(24) z(i, 1:natom)
  end do

  ! close dcd file
  close(24)
end subroutine read_dcd
