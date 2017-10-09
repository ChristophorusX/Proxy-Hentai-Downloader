import scala.util.matching.Regex
import scala.io.Source
import java.io.File
import java.io.PrintWriter

object Extractor {
  def main(args: Array[String]): Unit = {
    val urlFile = new File("/Users/christophorus/Desktop/Proxy-Hentai-Downloader/urls.txt")
    val urlBufferWriter = new PrintWriter(urlFile)
    // for (i <- 0 to 16) {
    //   val documentName = "view-source_https___exhentai.org_favorites.php_page=" + i + ".html"
    //   println("Now parsing document " + documentName)
    //   val resultUrlList = parse(documentName)
    //   urlBufferWriter.write(" " + resultUrlList)
    //   println("Document " + documentName + " has been parsed!")
    // }
    val documentName = "view-source_https___exhentai.org_favorites.php.html"
    println("Now parsing document " + documentName)
    val resultUrlList = parse(documentName)
    urlBufferWriter.write(" " + resultUrlList)
    println("Document " + documentName + " has been parsed!")
    urlBufferWriter.close()
  }

  def parse(documentName: String): String = {
    val pattern = new Regex("https://exhentai.org/g/[0-9]+/[0-9a-z]{10}/")
    val bufferSource = Source.fromFile("/Users/christophorus/Downloads/php/" + documentName)
    var returnString = ""
    for (line <- bufferSource.getLines()) {
        val iter = pattern findAllIn line
        returnString += iter filter (x => x equals iter.next) mkString (" ")
    }
    returnString
  }
}
