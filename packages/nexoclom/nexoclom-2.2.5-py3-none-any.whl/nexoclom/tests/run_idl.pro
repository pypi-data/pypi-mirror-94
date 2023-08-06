inputfiles = [$;'Ca.isotropic.maxwellian.50000.IDL.input', $
              $;'Ca.spot.maxwellian.IDL.input',           $
              $;'Na.Gaussian.4_2.south.IDL.input',       $
              'Na.Sputtering.IDL.input',              $
              'Ca.Gaussian.4_2.south.IDL.input',     $
              'Ca.spot.gaussian.IDL.input',         $
              'Na.Gaussian.3_1.IDL.input',         $
              'Na.Gaussian.3_1.no_accom.IDL.input'] 

for i=0,n_elements(inputfiles)-1 do begin
    run_idl_version, 'inputfiles/' + inputfiles[i]
endfor

end
