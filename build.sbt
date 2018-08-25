scalaVersion := "0.9.0-RC1"
scalacOptions ++= { if (isDotty.value) Seq("-language:Scala2") else Nil }
// libraryDependencies += ("a" %% "b" % "c").withDottyCompat(scalaVersion.value)
