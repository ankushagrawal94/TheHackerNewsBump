#This file is responsible for downloading all of the data.

require 'open-uri'
require 'zlib'

#expect 500B - 124MB per file. Downloading in incrememnts of 5000 should be safe.
startAt = 10643
stopAt = 10655
counter = 0
iSaved = 0
for yy in 11.. 14
	for mm in 1 .. 12
		for dd in 1 .. 31
			for hh in 0 .. 23
				counter += 1
				if counter < startAt
					next	
				end
				if counter > stopAt
					next
				end
				strHH = hh.to_s
				strDD = dd.to_s
				strMM = mm.to_s
				strYY = yy.to_s
				if strDD.length == 1
					strDD = "0" + strDD
				end
				if strMM.length == 1
					strMM = "0" + strMM
				end
				puts " #{yy} #{mm} #{dd} #{hh}"
				puts "currently on record #{counter} of #{stopAt}"
				puts "http://data.githubarchive.org/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json.gz"
				begin
					gz = open("http://data.githubarchive.org/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json.gz")
					puts "completed download"
					js = Zlib::GzipReader.new(gz).read
					File.open("/Volumes/WD_1TB/GitHub Archive/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json", 'w') do |f2|
						f2.puts js
					end
					iSaved += 1
					puts "file saved"
					f2.close
				rescue
					puts "Skipped: http://data.githubarchive.org/20"+strYY+"-"+strMM+"-"+strDD+"-"+strHH+".json.gz"
				ensure
					puts ""
				end
			end
		end
	end
end

totalPrinted = stopAt - startAt
puts "You saved a total of #{iSaved} docs."
puts "You started at #{startAt}"
puts "You stopped at #{stopAt}"





