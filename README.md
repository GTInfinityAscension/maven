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

The jars are the exact files attached to each GitHub release (reobfuscated, as players get them). Every 6 hours (or by hand, from the Actions tab) the `Sync releases` workflow publishes any new release of the mods listed in `artifacts.json`. To add a mod, add a line there. A published version is never overwritten. Only the newest 5 versions of each artifact are kept (GitHub Pages sites are limited to about 1 GB).
