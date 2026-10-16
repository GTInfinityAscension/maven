# GTInfinityAscension Maven

Maven repository for the organisation's mods, served by GitHub Pages at **https://gtinfinityascension.github.io/maven/**. No login is needed to download.

```groovy
repositories {
    maven { url = 'https://gtinfinityascension.github.io/maven/' }
}

dependencies {
    modCompileOnly("com.raishxn.gtna:gtna:0.6.0")
}
```

| Artifact | Repository |
| --- | --- |
| `com.raishxn.gtna:gtna` | [GregTech-Nexus-Addon](https://github.com/GTInfinityAscension/GregTech-Nexus-Addon) |

The jars are the exact files attached to each GitHub release (reobfuscated, as players get them). Each mod's `Maven` workflow adds a version when a release is published, through `tools/deploy.py`. A published version is never overwritten.
