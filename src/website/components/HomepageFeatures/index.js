import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: (
      <a href="/docs/modules" className={styles.modulesButton}>
        Modules
      </a>
    ),
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        Explore specialized modules covering critical technologies in Physical AI:
        ROS 2, Digital Twins, AI Robot Brains, and Vision-Language-Action systems.
      </>
    ),
  },
  {
    title: (
      <a href="/docs/physical-ai-humanoid-robotics/chapter-1/lesson-1-1-foundations-of-physical-ai" className={styles.chaptersButton}>
        Chapters
      </a>
    ),
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Comprehensive curriculum organized into 4 chapters covering all aspects
        of Physical AI and Humanoid Robotics, from foundations to advanced topics.
      </>
    ),
  },
  {
    title: (
      <a href="/docs/research-articles" className={styles.researchButton}>
        Research
      </a>
    ),
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        Key research articles and findings in Physical AI and Humanoid Robotics,
        covering breakthrough research and ongoing challenges in embodied AI systems.
      </>
    ),
  },
  {
    title: (
      <a href="/blog" className={styles.blogsButton}>
        Blogs
      </a>
    ),
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        Insights and articles on the evolution of humanoid robotics, industry trends,
        and expert perspectives on the future of Physical AI.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
